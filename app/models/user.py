import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # State tracking
    is_active = Column(Boolean(), default=True)
    current_mood = Column(String, nullable=True)
    battery_level = Column(String, nullable=True)
    
    # Relationship with couple
    couple_id = Column(UUID(as_uuid=True), ForeignKey("couples.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Backref relationships (will define later)
    couple = relationship("Couple", back_populates="partners", foreign_keys=[couple_id])
