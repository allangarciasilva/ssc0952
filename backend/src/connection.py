import json
from collections import defaultdict
from typing import Any

from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, room_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: int, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]

    async def broadcast(self, room_id: int, message: Any):
        message = json.dumps({
            "active_connections": len(self.active_connections[room_id]),
            "message": message
        })
        for connection in self.active_connections[room_id]:
            await connection.send_text(message)
