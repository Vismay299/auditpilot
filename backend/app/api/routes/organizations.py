"""
Organization endpoints (for dev/bootstrap; multi-tenant).
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.organization import Organization

router = APIRouter(prefix="/organizations", tags=["organizations"])


class OrganizationCreateBody(BaseModel):
    name: str
    slug: str


class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str

    class Config:
        from_attributes = True


@router.post("", response_model=OrganizationResponse)
def create_organization(body: OrganizationCreateBody, db: Session = Depends(get_db)):
    """Create an organization (e.g. for dev). Use returned id as X-Org-Id header."""
    existing = db.query(Organization).filter(Organization.slug == body.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    org = Organization(name=body.name, slug=body.slug)
    db.add(org)
    db.commit()
    db.refresh(org)
    return OrganizationResponse(id=str(org.id), name=org.name, slug=org.slug)


@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: UUID, db: Session = Depends(get_db)):
    """Get organization by id."""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return OrganizationResponse(id=str(org.id), name=org.name, slug=org.slug)
