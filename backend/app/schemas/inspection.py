from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class InspectionBase(BaseModel):
    name: str
    site_location: Optional[str] = None
    site_address: Optional[str] = None
    inspector_id: Optional[UUID] = None

class InspectionCreate(InspectionBase):
    org_id: UUID

class InspectionUpdate(BaseModel):
    name: Optional[str] = None
    site_location: Optional[str] = None
    site_address: Optional[str] = None
    status: Optional[str] = None
    risk_level: Optional[str] = None
    report_narrative: Optional[str] = None

class Inspection(InspectionBase):
    id: UUID
    org_id: UUID
    status: str
    risk_level: Optional[str] = None
    report_narrative: Optional[str] = None
    total_findings: int
    total_files: int
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
