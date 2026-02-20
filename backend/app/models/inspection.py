from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, CheckConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    site_location = Column(String)
    site_address = Column(String)
    inspector_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(String, default="processing")
    risk_level = Column(String)
    report_narrative = Column(Text)
    total_findings = Column(Integer, default=0)
    total_files = Column(Integer, default=0)
    processing_started_at = Column(DateTime(timezone=True))
    processing_completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('processing', 'review', 'completed', 'failed')", name="check_status"),
        CheckConstraint("risk_level IN ('critical', 'high', 'medium', 'low', 'clear') OR risk_level IS NULL", name="check_risk_level"),
    )

    organization = relationship("Organization", backref="inspections")
    inspector = relationship("User", backref="inspections")
    files = relationship("File", back_populates="inspection", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="inspection", cascade="all, delete-orphan")
