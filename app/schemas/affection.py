from pydantic import BaseModel, UUID4
from datetime import datetime

class AffectionCreate(BaseModel):
    type: str # kiss, hug, thinking, miss

class AffectionResponse(BaseModel):
    id: UUID4
    type: str
    sender_id: UUID4
    couple_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True
