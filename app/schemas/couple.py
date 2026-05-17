from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import datetime
from .user import User

class CoupleBase(BaseModel):
    anniversary_date: Optional[datetime] = None

class CoupleCreate(CoupleBase):
    pass

class CoupleInDBBase(CoupleBase):
    id: UUID4
    invite_code: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Couple(CoupleInDBBase):
    partners: List[User] = []
