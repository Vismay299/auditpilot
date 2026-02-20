"""
Track file and inspection processing status for the worker and API.
"""
import logging
from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.file_repository import FileRepository
from app.repositories.finding_repository import FindingRepository
from app.repositories.inspection_repository import InspectionRepository
from app.models.file import File

logger = logging.getLogger(__name__)


class JobTracker:
    def __init__(self, db: Session):
        self.db = db
        self.file_repo = FileRepository(db)
        self.finding_repo = FindingRepository(db)
        self.inspection_repo = InspectionRepository(db)

    def update_file_status(
        self,
        file_id: UUID,
        status: str,
        error_message: str | None = None,
    ) -> File | None:
        return self.file_repo.update_status(file_id, status, error_message=error_message)

    def update_inspection_progress(self, inspection_id: UUID) -> None:
        total = self.file_repo.total_count_by_inspection(inspection_id)
        completed = self.file_repo.count_by_inspection_and_status(inspection_id, "completed")
        failed = self.file_repo.count_by_inspection_and_status(inspection_id, "failed")
        if total == 0:
            return
        if completed + failed >= total:
            finding_count = self.finding_repo.count_by_inspection(inspection_id)
            self.inspection_repo.update_status(
                inspection_id,
                "completed" if failed == 0 else "review",
                total_findings=finding_count,
                total_files=total,
            )
        return None

    def log_processing_step(self, file_id: str, step: str, duration_seconds: float) -> None:
        logger.info("file_id=%s step=%s duration=%.2fs", file_id, step, duration_seconds)
