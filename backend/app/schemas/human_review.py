from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class HumanReviewBase(BaseModel):
    original_category: str
    corrected_category: str
    original_severity: Optional[str] = None
    corrected_severity: Optional[str] = None
    notes: Optional[str] = None
    review_duration_seconds: Optional[int] = None

class HumanReviewCreate(HumanReviewBase):
    finding_id: UUID
    reviewer_id: Optional[UUID] = None

class HumanReview(HumanReviewBase):
    id: UUID
    finding_id: UUID
    reviewer_id: Optional[UUID] = None
    reviewed_at: datetime

    class Config:
        from_attributes = True
