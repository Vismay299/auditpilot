"""
Inspection CRUD endpoints.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.auth import get_org_id
from app.repositories.inspection_repository import InspectionRepository
from app.models.inspection import Inspection
from app.models.finding import Finding
from sqlalchemy import func

router = APIRouter(prefix="/inspections", tags=["inspections"])


class InspectionCreateBody(BaseModel):
    name: str
    site_location: str | None = None
    site_address: str | None = None


class InspectionResponse(BaseModel):
    id: str
    name: str
    status: str
    org_id: str
    site_location: str | None
    site_address: str | None
    total_files: int
    total_findings: int
    risk_level: str | None = None
    report_narrative: str | None = None

    class Config:
        from_attributes = True


@router.get("", response_model=list[InspectionResponse])
def list_inspections(
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
    limit: int = 50,
):
    """List inspections for the current org (most recent first)."""
    repo = InspectionRepository(db)
    inspections = repo.list_by_org(org_id, limit=limit)
    return [
        InspectionResponse(
            id=str(i.id),
            name=i.name,
            status=i.status,
            org_id=str(i.org_id),
            site_location=i.site_location,
            site_address=i.site_address,
            total_files=i.total_files,
            total_findings=i.total_findings,
            risk_level=i.risk_level,
            report_narrative=i.report_narrative,
        )
        for i in inspections
    ]


@router.post("", response_model=InspectionResponse)
def create_inspection(
    body: InspectionCreateBody,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Create a new inspection for the current org."""
    repo = InspectionRepository(db)
    insp = repo.create(
        org_id=org_id,
        name=body.name,
        site_location=body.site_location,
        site_address=body.site_address,
    )
    return InspectionResponse(
        id=str(insp.id),
        name=insp.name,
        status=insp.status,
        org_id=str(insp.org_id),
        site_location=insp.site_location,
        site_address=insp.site_address,
        total_files=insp.total_files,
        total_findings=insp.total_findings,
        risk_level=insp.risk_level,
        report_narrative=insp.report_narrative,
    )


@router.get("/stats")
def get_inspection_stats(
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Aggregate stats for the dashboard."""
    # Total inspections in org
    total_inspections = db.query(func.count(Inspection.id)).filter(Inspection.org_id == org_id).scalar() or 0
    
    # Total findings across all inspections in org
    total_findings = (
        db.query(func.count(Finding.id))
        .join(Inspection, Finding.inspection_id == Inspection.id)
        .filter(Inspection.org_id == org_id)
        .scalar()
    ) or 0
    
    # Pending reviews (findings needing review)
    pending_reviews = (
        db.query(func.count(Finding.id))
        .join(Inspection, Finding.inspection_id == Inspection.id)
        .filter(Inspection.org_id == org_id, Finding.needs_review == True)
        .scalar()
    ) or 0

    return {
        "totalInspections": total_inspections,
        "totalFindings": total_findings,
        "pendingReviews": pending_reviews,
        "avgProcessingTime": "N/A",  # Could be calculated later
    }


@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(
    inspection_id: UUID,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Get inspection by id (org-scoped)."""
    repo = InspectionRepository(db)
    insp = repo.get_by_id(inspection_id, org_id=org_id)
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return InspectionResponse(
        id=str(insp.id),
        name=insp.name,
        status=insp.status,
        org_id=str(insp.org_id),
        site_location=insp.site_location,
        site_address=insp.site_address,
        total_files=insp.total_files,
        total_findings=insp.total_findings,
        risk_level=insp.risk_level,
        report_narrative=insp.report_narrative,
    )
