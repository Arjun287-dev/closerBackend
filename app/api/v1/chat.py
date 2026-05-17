from typing import Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.message import Message
from app.websockets.manager import manager

router = APIRouter()

@router.websocket("/ws/{couple_id}")
async def websocket_endpoint(websocket: WebSocket, couple_id: str, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket, couple_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Expected data: {"content": "hello", "sender_id": "uuid", "message_type": "text"}
            
            # Save message to DB
            new_message = Message(
                content=data["content"],
                message_type=data.get("message_type", "text"),
                sender_id=data["sender_id"],
                couple_id=couple_id
            )
            db.add(new_message)
            await db.commit()
            
            # Broadcast to partner
            await manager.broadcast_to_couple(data, couple_id, sender_ws=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, couple_id)
