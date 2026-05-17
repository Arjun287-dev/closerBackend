from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    current_mood: Optional[str] = None
    battery_level: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID4
    is_active: bool
    current_mood: Optional[str] = None
    battery_level: Optional[str] = None
    couple_id: Optional[UUID4] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass
