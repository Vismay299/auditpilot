from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

class FindingBase(BaseModel):
    category: str
    severity: Optional[str] = None
    confidence_score: Optional[float] = None
    needs_review: bool = False
    description: Optional[str] = None
    ai_caption: Optional[str] = None
    transcription: Optional[str] = None
    location_code: Optional[str] = None
    equipment_id: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = {}

class FindingCreate(FindingBase):
    inspection_id: UUID
    file_id: Optional[UUID] = None

class FindingUpdate(BaseModel):
    category: Optional[str] = None
    severity: Optional[str] = None
    confidence_score: Optional[float] = None
    needs_review: Optional[bool] = None
    description: Optional[str] = None

class Finding(FindingBase):
    id: UUID
    inspection_id: UUID
    file_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
