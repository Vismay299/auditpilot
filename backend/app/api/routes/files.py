"""
File upload and metadata endpoints.
"""
import mimetypes
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_org_id
from app.services.storage_service import upload_file as storage_upload, generate_presigned_url
from app.repositories.inspection_repository import InspectionRepository
from app.repositories.file_repository import FileRepository
from app.workers.file_processor import process_file_background

router = APIRouter(tags=["files"])

ALLOWED_IMAGE = {"image/jpeg", "image/png", "image/jpg"}
ALLOWED_AUDIO = {"audio/mpeg", "audio/mp3", "audio/m4a", "audio/x-m4a", "audio/wav"}
ALLOWED_PDF = {"application/pdf"}
ALLOWED = ALLOWED_IMAGE | ALLOWED_AUDIO | ALLOWED_PDF
MAX_SIZE = 50 * 1024 * 1024  # 50MB


def _file_type_from_mime(mime: str | None, filename: str) -> str:
    if mime in ALLOWED_IMAGE:
        return "image"
    if mime in ALLOWED_AUDIO:
        return "audio"
    if mime in ALLOWED_PDF:
        return "pdf"
    if filename and filename.lower().endswith((".jpg", ".jpeg", ".png")):
        return "image"
    if filename and filename.lower().endswith((".mp3", ".m4a", ".wav")):
        return "audio"
    if filename and filename.lower().endswith(".pdf"):
        return "pdf"
    return "other"


@router.post("/inspections/{inspection_id}/files")
async def upload_files(
    inspection_id: UUID,
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Upload one or more files for an inspection. Files are stored and processed in the background."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    insp_repo = InspectionRepository(db)
    file_repo = FileRepository(db)
    inspection = insp_repo.get_by_id(inspection_id, org_id=org_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")

    org_str = str(org_id)
    insp_str = str(inspection_id)
    created = []
    for upload in files:
        if upload.size and upload.size > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File {upload.filename} exceeds 50MB limit",
            )
        mime = upload.content_type or mimetypes.guess_type(upload.filename or "")[0]
        if mime not in ALLOWED and _file_type_from_mime(mime, upload.filename or "") == "other":
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed: {upload.filename}. Use image, audio, or PDF.",
            )
        key, url = await storage_upload(upload, org_str, insp_str)
        file_type = _file_type_from_mime(mime, upload.filename or "")
        rec = file_repo.create(
            inspection_id=inspection_id,
            file_type=file_type,
            file_name=upload.filename or "file",
            storage_url=url,
            storage_key=key,
            file_size=upload.size,
            mime_type=mime,
        )
        background_tasks.add_task(process_file_background, str(rec.id), file_type, insp_str)
        created.append({"id": str(rec.id), "file_name": rec.file_name, "status": rec.status})
    return {"files": created}


@router.get("/inspections/{inspection_id}/files")
def list_files(
    inspection_id: UUID,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """List all files for an inspection."""
    insp_repo = InspectionRepository(db)
    file_repo = FileRepository(db)
    inspection = insp_repo.get_by_id(inspection_id, org_id=org_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    files = file_repo.list_by_inspection(inspection_id)
    return {
        "files": [
            {
                "id": str(f.id),
                "file_name": f.file_name,
                "file_type": f.file_type,
                "status": f.status,
                "file_size": f.file_size,
                "created_at": f.created_at.isoformat() if f.created_at else None,
            }
            for f in files
        ]
    }


@router.get("/files/{file_id}")
def get_file_metadata(
    file_id: UUID,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Get file metadata and optional download URL."""
    from app.models.inspection import Inspection
    file_repo = FileRepository(db)
    f = file_repo.get_by_id(file_id)
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    inspection = db.query(Inspection).filter(
        Inspection.id == f.inspection_id,
        Inspection.org_id == org_id,
    ).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="File not found")
    presigned = generate_presigned_url(f.storage_key) if f.storage_key else None
    return {
        "id": str(f.id),
        "file_name": f.file_name,
        "file_type": f.file_type,
        "status": f.status,
        "file_size": f.file_size,
        "mime_type": f.mime_type,
        "inspection_id": str(f.inspection_id),
        "download_url": presigned,
        "created_at": f.created_at.isoformat() if f.created_at else None,
    }