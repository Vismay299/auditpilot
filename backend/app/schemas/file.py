from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class FileBase(BaseModel):
    file_type: str
    file_name: str
    storage_url: str
    storage_key: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

class FileCreate(FileBase):
    inspection_id: UUID

class FileUpdate(BaseModel):
    status: Optional[str] = None
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None

class File(FileBase):
    id: UUID
    inspection_id: UUID
    status: str
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
