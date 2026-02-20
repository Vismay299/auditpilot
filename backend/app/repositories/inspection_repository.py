from uuid import UUID
from sqlalchemy.orm import Session
from app.models.inspection import Inspection

class InspectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, inspection_id: UUID, org_id: UUID | None = None) -> Inspection | None:
        q = self.db.query(Inspection).filter(Inspection.id == inspection_id)
        if org_id is not None:
            q = q.filter(Inspection.org_id == org_id)
        return q.first()

    def create(self, org_id: UUID, name: str, **kwargs) -> Inspection:
        insp = Inspection(org_id=org_id, name=name, **kwargs)
        self.db.add(insp)
        self.db.commit()
        self.db.refresh(insp)
        return insp

    def list_by_org(self, org_id: UUID, limit: int = 50) -> list[Inspection]:
        return (
            self.db.query(Inspection)
            .filter(Inspection.org_id == org_id)
            .order_by(Inspection.created_at.desc())
            .limit(limit)
            .all()
        )

    def update_status(self, inspection_id: UUID, status: str, **kwargs) -> Inspection | None:
        insp = self.db.query(Inspection).filter(Inspection.id == inspection_id).first()
        if not insp:
            return None
        insp.status = status
        for k, v in kwargs.items():
            if hasattr(insp, k):
                setattr(insp, k, v)
        self.db.commit()
        self.db.refresh(insp)
        return insp