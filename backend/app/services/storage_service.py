"""
Storage service for file upload/download.
Uses local filesystem storage.
"""
import os
import uuid
import tempfile
from pathlib import Path
from fastapi import UploadFile

# Local upload directory (configurable via env)
LOCAL_UPLOAD_DIR = Path(os.getenv("LOCAL_UPLOAD_DIR", tempfile.gettempdir())) / "auditpilot_uploads"
LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _object_key(org_id: str, inspection_id: str, file_name: str) -> str:
    """Generate unique storage key: org/inspection/uuid_filename."""
    ext = Path(file_name).suffix
    unique = f"{uuid.uuid4().hex}{ext}"
    return f"{org_id}/{inspection_id}/{unique}"


async def upload_file(
    file: UploadFile,
    org_id: str,
    inspection_id: str,
) -> tuple[str, str]:
    """
    Upload file to local filesystem. Returns (storage_key, storage_url).
    """
    key = _object_key(org_id, inspection_id, file.filename or "file")
    content = await file.read()

    local_path = LOCAL_UPLOAD_DIR / key.replace("/", os.sep)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_bytes(content)
    return key, str(local_path)


async def download_file(storage_key: str) -> bytes:
    """Download file bytes by storage key."""
    local_path = LOCAL_UPLOAD_DIR / storage_key.replace("/", os.sep)
    if not local_path.exists():
        raise FileNotFoundError(f"File not found: {storage_key}")
    return local_path.read_bytes()


async def delete_file(storage_key: str) -> None:
    """Delete file from storage."""
    local_path = LOCAL_UPLOAD_DIR / storage_key.replace("/", os.sep)
    if local_path.exists():
        local_path.unlink()


def generate_presigned_url(storage_key: str, expiration: int = 3600) -> str:
    """Return local file path (no presigned URLs for local storage)."""
    local_path = LOCAL_UPLOAD_DIR / storage_key.replace("/", os.sep)
    return str(local_path)
