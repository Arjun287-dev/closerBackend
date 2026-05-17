import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Couple(Base):
    __tablename__ = "couples"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    anniversary_date = Column(DateTime(timezone=True), nullable=True)
    invite_code = Column(String, unique=True, index=True, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Partners relationship
    partners = relationship("User", back_populates="couple", foreign_keys="User.couple_id")
