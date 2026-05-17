from typing import Dict, List
import json
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Maps couple_id to a list of active websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, couple_id: str):
        await websocket.accept()
        if couple_id not in self.active_connections:
            self.active_connections[couple_id] = []
        self.active_connections[couple_id].append(websocket)

    def disconnect(self, websocket: WebSocket, couple_id: str):
        if couple_id in self.active_connections:
            self.active_connections[couple_id].remove(websocket)
            if not self.active_connections[couple_id]:
                del self.active_connections[couple_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_to_couple(self, message: dict, couple_id: str, sender_ws: WebSocket = None):
        if couple_id in self.active_connections:
            for connection in self.active_connections[couple_id]:
                if connection != sender_ws:
                    await connection.send_json(message)

manager = ConnectionManager()
