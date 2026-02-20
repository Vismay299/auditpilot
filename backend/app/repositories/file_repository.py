from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.file import File
from app.models.inspection import Inspection

class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        inspection_id: UUID,
        file_type: str,
        file_name: str,
        storage_url: str,
        storage_key: str,
        file_size: int | None = None,
        mime_type: str | None = None,
    ) -> File:
        f = File(
            inspection_id=inspection_id,
            file_type=file_type,
            file_name=file_name,
            storage_url=storage_url,
            storage_key=storage_key,
            file_size=file_size,
            mime_type=mime_type,
            status="pending",
        )
        self.db.add(f)
        self.db.commit()
        self.db.refresh(f)
        return f

    def get_by_id(self, file_id: UUID) -> File | None:
        return self.db.query(File).filter(File.id == file_id).first()

    def list_by_inspection(self, inspection_id: UUID) -> list[File]:
        return self.db.query(File).filter(File.inspection_id == inspection_id).all()

    def update_status(
        self,
        file_id: UUID,
        status: str,
        error_message: str | None = None,
        processed_at: datetime | None = None,
    ) -> File | None:
        f = self.db.query(File).filter(File.id == file_id).first()
        if not f:
            return None
        f.status = status
        if error_message is not None:
            f.error_message = error_message
        if processed_at is not None:
            f.processed_at = processed_at
        elif status == "completed":
            f.processed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(f)
        return f

    def count_by_inspection_and_status(self, inspection_id: UUID, status: str) -> int:
        return self.db.query(File).filter(
            File.inspection_id == inspection_id,
            File.status == status,
        ).count()

    def total_count_by_inspection(self, inspection_id: UUID) -> int:
        return self.db.query(File).filter(File.inspection_id == inspection_id).count()