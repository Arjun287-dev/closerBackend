import string
import random
from typing import Any, Optional
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

@router.post("/mood")
async def update_mood(
    mood: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    current_user.current_mood = mood
    db.add(current_user)
    await db.commit()
    return {"status": "success", "mood": mood}

@router.post("/battery")
async def update_battery(
    level: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    current_user.battery_level = level
    db.add(current_user)
    await db.commit()
    return {"status": "success", "battery_level": level}

@router.post("/meetup")
async def update_meetup(
    meetup_date: str, # ISO string format
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="User not in a couple")
    
    result = await db.execute(select(Couple).filter(Couple.id == current_user.couple_id))
    couple = result.scalars().first()
    if not couple:
        raise HTTPException(status_code=404, detail="Couple not found")
    
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(meetup_date.replace("Z", "+00:00"))
        couple.next_meetup_date = dt
        db.add(couple)
        await db.commit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
        
    return {"status": "success", "next_meetup_date": couple.next_meetup_date}

@router.get("/status")
async def get_couple_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user.couple_id:
        return {
            "in_couple": False,
            "partner_name": None,
            "partner_mood": None,
            "partner_battery": None,
            "next_meetup": None
        }
    
    # Get partner
    result = await db.execute(
        select(User).filter(User.couple_id == current_user.couple_id, User.id != current_user.id)
    )
    partner = result.scalars().first()
    
    # Get couple info
    couple_result = await db.execute(select(Couple).filter(Couple.id == current_user.couple_id))
    couple = couple_result.scalars().first()
    
    return {
        "in_couple": True,
        "partner_name": partner.name if partner else "Waiting for partner...",
        "partner_mood": partner.current_mood if partner else "Unknown",
        "partner_battery": partner.battery_level if partner else "100%",
        "next_meetup": couple.next_meetup_date if couple else None
    }

from app.models.affection import Affection
from app.schemas.affection import AffectionCreate, AffectionResponse

@router.post("/affection", response_model=AffectionResponse)
async def send_affection(
    affection_in: AffectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="User not in a couple")
    
    affection = Affection(
        type=affection_in.type,
        sender_id=current_user.id,
        couple_id=current_user.couple_id
    )
    db.add(affection)
    await db.commit()
    await db.refresh(affection)
    return affection

@router.get("/affection/latest", response_model=Optional[AffectionResponse])
async def get_latest_affection(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user.couple_id:
        return None
        
    result = await db.execute(
        select(Affection)
        .filter(Affection.couple_id == current_user.couple_id, Affection.sender_id != current_user.id)
        .order_by(Affection.created_at.desc())
        .limit(1)
    )
    return result.scalars().first()
