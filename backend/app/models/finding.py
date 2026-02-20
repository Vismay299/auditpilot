from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, CheckConstraint, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid
from app.core.database import Base

class Finding(Base):
    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inspection_id = Column(UUID(as_uuid=True), ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"))
    category = Column(String, nullable=False)
    severity = Column(String)
    confidence_score = Column(Float)
    needs_review = Column(Boolean, default=False)
    description = Column(Text)
    ai_caption = Column(Text)
    transcription = Column(Text)
    location_code = Column(String)
    equipment_id = Column(String)
    extra_metadata = Column(JSONB, default={})
    embedding = Column(Vector(384))  # pgvector column
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("severity IN ('critical', 'high', 'medium', 'low', 'clear') OR severity IS NULL", name="check_severity"),
        CheckConstraint("confidence_score >= 0 AND confidence_score <= 1", name="check_confidence_score"),
    )

    inspection = relationship("Inspection", back_populates="findings")
    file = relationship("File", back_populates="findings")
    reviews = relationship("HumanReview", back_populates="finding", cascade="all, delete-orphan")
