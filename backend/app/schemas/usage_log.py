from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class UsageLogBase(BaseModel):
    model_name: str
    task_type: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    processing_time_ms: Optional[int] = None
    cost_usd: Optional[Decimal] = None

class UsageLogCreate(UsageLogBase):
    inspection_id: UUID
    file_id: Optional[UUID] = None

class UsageLog(UsageLogBase):
    id: UUID
    inspection_id: UUID
    file_id: Optional[UUID] = None
    timestamp: datetime

    class Config:
        from_attributes = True
