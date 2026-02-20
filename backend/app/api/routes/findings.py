"""
Findings API route: list findings for an inspection.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_org_id
from app.repositories.finding_repository import FindingRepository
from app.repositories.inspection_repository import InspectionRepository
from app.models.finding import Finding
from app.models.inspection import Inspection
from sqlalchemy import func

router = APIRouter(tags=["findings"])


@router.get("/inspections/{inspection_id}/findings")
def list_findings(
    inspection_id: UUID,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Return all findings for an inspection."""
    insp_repo = InspectionRepository(db)
    inspection = insp_repo.get_by_id(inspection_id, org_id=org_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")

    finding_repo = FindingRepository(db)
    findings = finding_repo.list_by_inspection(inspection_id)

    return {
        "findings": [
            {
                "id": str(f.id),
                "file_id": str(f.file_id) if f.file_id else None,
                "category": f.category,
                "severity": f.severity,
                "confidence_score": f.confidence_score,
                "needs_review": f.needs_review,
                "description": f.description,
                "ai_caption": f.ai_caption,
                "transcription": f.transcription,
                "location_code": f.location_code,
                "equipment_id": f.equipment_id,
                "created_at": f.created_at.isoformat() if f.created_at else None,
            }
            for f in findings
        ]
    }


@router.get("/findings/stats")
def get_findings_stats(
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Aggregate findings by category across all org inspections."""
    stats = (
        db.query(Finding.category, func.count(Finding.id).label("count"))
        .join(Inspection, Finding.inspection_id == Inspection.id)
        .filter(Inspection.org_id == org_id)
        .group_by(Finding.category)
        .all()
    )
    
    # Map raw SQL category to something readable and assign predefined UI colors or let UI handle colors
    return [
        {"name": row.category.capitalize() if row.category else "Unknown", "value": row.count}
        for row in stats
    ]


@router.get("/findings/review-queue")
def get_review_queue(
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    """Return all findings that need human review across all org inspections."""
    items = (
        db.query(Finding, Inspection)
        .join(Inspection, Finding.inspection_id == Inspection.id)
        .filter(Inspection.org_id == org_id, Finding.needs_review == True)
        .order_by(Finding.created_at.desc())
        .limit(50)
        .all()
    )
    
    return [
        {
            "id": str(row.Finding.id),
            "ai_caption": row.Finding.ai_caption,
            "category": row.Finding.category,
            "confidence_score": row.Finding.confidence_score,
            "severity": row.Finding.severity,
            "inspection": {
                "id": str(row.Inspection.id),
                "name": row.Inspection.name,
            }
        }
        for row in items
    ]
