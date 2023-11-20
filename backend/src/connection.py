import json
from collections import defaultdict
from typing import Any, Optional

from starlette.websockets import WebSocket

from src.database import SessionLocal, models
from src.iot import crud


class ConnectionManager:
    def __init__(self):
        self.subscribers_by_topic: dict[str, set[WebSocket]] = defaultdict(set)
        self.db = SessionLocal()

    async def publish(self, topic: str, message: Any):
        for socket in self.subscribers_by_topic[topic]:
            await socket.send_json(message)

    async def publish_to_users(self, room_id: Optional[int], message: Any):
        if room_id is None:
            return
        for db_user in crud.get_subscribed_users(self.db, room_id):
            await self.publish(f"user/{db_user.id}", message)

    def subscribe(self, ws: WebSocket, *topics: str):
        print(f"Subscribed to {topics}")
        for topic in topics:
            self.subscribers_by_topic[topic].add(ws)

    def unsubscribe(self, ws: WebSocket, *topics: str):
        print(f"Unsubscribed from {topics}")
        for topic in topics:
            self.subscribers_by_topic[topic].remove(ws)

    async def on_device_setup(self, device_name: str, room_id: int):
        db_device = self.db.query(models.Device).filter_by(name=device_name).first()
        if db_device:
            db_device.active = True
            db_device.room_id = room_id
        else:
            db_device = models.Device(active=True, name=device_name, room_id=room_id)
            self.db.add(db_device)
        self.db.commit()
        await self.publish_to_users(
            db_device.room_id, f"The device {device_name} is now active."
        )

    async def on_device_shutdown(self, device_name: str):
        db_device = self.db.query(models.Device).filter_by(name=device_name).first()
        if db_device:
            db_device.active = False
        else:
            db_device = models.Device(active=False, name=device_name)
            self.db.add(db_device)
        self.db.commit()
        await self.publish_to_users(
            db_device.room_id, f"The device {device_name} is now inactive."
        )


connection_manager = ConnectionManager()
