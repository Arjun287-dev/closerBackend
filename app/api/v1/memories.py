from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.memory import Memory
from app.models.user import User
from app.schemas.memory import MemoryCreate, MemoryResponse
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[MemoryResponse])
async def list_memories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="User not in a couple")
    
    result = await db.execute(
        select(Memory)
        .filter(Memory.couple_id == current_user.couple_id)
        .order_by(Memory.created_at.desc())
    )
    return result.scalars().all()

@router.post("/", response_model=MemoryResponse)
async def create_memory(
    memory_in: MemoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="User not in a couple")
    
    memory = Memory(
        title=memory_in.title,
        description=memory_in.description,
        image_url=memory_in.image_url,
        couple_id=current_user.couple_id
    )
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory
