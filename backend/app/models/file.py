from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inspection_id = Column(UUID(as_uuid=True), ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    storage_url = Column(String, nullable=False)
    storage_key = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    status = Column(String, default="pending")
    error_message = Column(String)
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("file_type IN ('image', 'audio', 'pdf', 'other')", name="check_file_type"),
        CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed')", name="check_file_status"),
    )

    inspection = relationship("Inspection", back_populates="files")
    findings = relationship("Finding", back_populates="file", cascade="all, delete-orphan")
