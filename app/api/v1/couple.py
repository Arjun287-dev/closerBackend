import string
import random
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.couple import Couple
from app.schemas.couple import Couple as CoupleSchema, CoupleCreate
from app.api.deps import get_current_active_user

router = APIRouter()

def generate_invite_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@router.post("/invite", response_model=CoupleSchema)
async def create_invite(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if current_user.couple_id:
        raise HTTPException(status_code=400, detail="User already in a couple")
    
    # Create new couple with an invite code
    code = generate_invite_code()
    couple = Couple(invite_code=code)
    db.add(couple)
    await db.commit()
    await db.refresh(couple)
    
    # Update current user
    current_user.couple_id = couple.id
    db.add(current_user)
    await db.commit()
    await db.refresh(couple)
    
    return couple

@router.post("/accept", response_model=CoupleSchema)
async def accept_invite(
    invite_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if current_user.couple_id:
        raise HTTPException(status_code=400, detail="User already in a couple")
        
    result = await db.execute(select(Couple).filter(Couple.invite_code == invite_code))
    couple = result.scalars().first()
    
    if not couple:
        raise HTTPException(status_code=404, detail="Invalid invite code")
        
    current_user.couple_id = couple.id
    # Once accepted, maybe invalidate the invite code to prevent others from using it
    couple.invite_code = None 
    db.add(current_user)
    db.add(couple)
    await db.commit()
    await db.refresh(couple)
    
    return couple
