import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Affection(Base):
    __tablename__ = "affections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    type = Column(String, nullable=False) # kiss, hug, thinking, miss
    
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    couple_id = Column(UUID(as_uuid=True), ForeignKey("couples.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    couple = relationship("Couple", foreign_keys=[couple_id])
