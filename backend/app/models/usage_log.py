from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inspection_id = Column(UUID(as_uuid=True), ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"))
    model_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    processing_time_ms = Column(Integer)
    cost_usd = Column(Numeric(10, 6))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    inspection = relationship("Inspection", backref="usage_logs")
    file = relationship("File", backref="usage_logs")
