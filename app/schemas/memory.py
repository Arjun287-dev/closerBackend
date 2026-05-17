from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class MemoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class MemoryCreate(MemoryBase):
    pass

class MemoryResponse(MemoryBase):
    id: UUID4
    couple_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True
