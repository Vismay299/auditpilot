from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class HumanReview(Base):
    __tablename__ = "human_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    finding_id = Column(UUID(as_uuid=True), ForeignKey("findings.id", ondelete="CASCADE"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    original_category = Column(String, nullable=False)
    corrected_category = Column(String, nullable=False)
    original_severity = Column(String)
    corrected_severity = Column(String)
    notes = Column(String)
    review_duration_seconds = Column(Integer)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    finding = relationship("Finding", back_populates="reviews")
    reviewer = relationship("User", backref="reviews")
