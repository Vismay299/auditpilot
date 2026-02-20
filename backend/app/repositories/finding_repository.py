"""
Repository for Finding CRUD operations.
"""
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.finding import Finding


class FindingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        inspection_id: UUID,
        file_id: UUID,
        category: str,
        severity: str | None = None,
        confidence_score: float | None = None,
        needs_review: bool = False,
        description: str | None = None,
        ai_caption: str | None = None,
        transcription: str | None = None,
        location_code: str | None = None,
        equipment_id: str | None = None,
        extra_metadata: dict | None = None,
        embedding: list[float] | None = None,
    ) -> Finding:
        finding = Finding(
            inspection_id=inspection_id,
            file_id=file_id,
            category=category,
            severity=severity,
            confidence_score=confidence_score,
            needs_review=needs_review,
            description=description,
            ai_caption=ai_caption,
            transcription=transcription,
            location_code=location_code,
            equipment_id=equipment_id,
            extra_metadata=extra_metadata or {},
            embedding=embedding,
        )
        self.db.add(finding)
        self.db.commit()
        self.db.refresh(finding)
        return finding

    def get_by_id(self, finding_id: UUID) -> Finding | None:
        return self.db.query(Finding).filter(Finding.id == finding_id).first()

    def list_by_inspection(self, inspection_id: UUID) -> list[Finding]:
        return (
            self.db.query(Finding)
            .filter(Finding.inspection_id == inspection_id)
            .order_by(Finding.created_at.desc())
            .all()
        )

    def count_by_inspection(self, inspection_id: UUID) -> int:
        return self.db.query(Finding).filter(Finding.inspection_id == inspection_id).count()
