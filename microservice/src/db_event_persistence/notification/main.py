import traceback

import uvloop
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from orjson import orjson
from sqlalchemy.orm import Session

from src.room_manager.rooms import crud
from src.shared.database import models
from src.shared.database.connection import SessionLocal
from src.shared.settings import SETTINGS


def get_or_create_device_by_name(db: Session, device_name: str):
    db_device = db.query(models.Device).filter_by(name=device_name).first()
    if not db_device:
        db_device = models.Device(active=True, name=device_name)
        db.add(db_device)
    return db_device


async def publish_notification_to_users(kafka_producer: AIOKafkaProducer, db: Session, room_id: int,
                                        message: str):
    for user in crud.get_subscribed_users(db, room_id):
        print(f"Sending notification to user {user.id}: {message}")
        await kafka_producer.send_and_wait("notification", key=orjson.dumps(user.id), value=orjson.dumps(message))


async def on_device_setup(kafka_producer: AIOKafkaProducer, db: Session, device_name: str, room_id: int):
    db_device = get_or_create_device_by_name(db, device_name)
    db_device.active = True
    db_device.room_id = room_id
    db.commit()

    db.refresh(db_device)
    message = f"Device {device_name} is now active at room {db_device.room.name}."
    await publish_notification_to_users(kafka_producer, db, db_device.room_id, message)


async def on_device_shutdown(kafka_producer: AIOKafkaProducer, db: Session, device_name: str):
    db_device = get_or_create_device_by_name(db, device_name)
    db_device.active = False
    db.commit()

    db.refresh(db_device)
    message = f"Device {device_name} is no longer active at room {db_device.room.name}."
    await publish_notification_to_users(kafka_producer, db, db_device.room_id, message)


async def listen_to_notifications():
    db = SessionLocal()

    producer = AIOKafkaProducer(bootstrap_servers=SETTINGS.kafka_server)
    await producer.start()

    consumer = AIOKafkaConsumer('setup', 'shutdown', bootstrap_servers=SETTINGS.kafka_server,
                                group_id="notification-consumer")
    await consumer.start()

    try:
        async for msg in consumer:
            try:
                if msg.topic == "setup":
                    await on_device_setup(producer, db, msg.key.decode(), orjson.loads(msg.value)["room_id"])
                else:
                    await on_device_shutdown(producer, db, msg.key.decode())
            except Exception:
                traceback.print_exc()
    finally:
        await producer.stop()
        await consumer.stop()


if __name__ == "__main__":
    print("Starting notification pesistence")
    try:
        uvloop.run(listen_to_notifications())
    except KeyboardInterrupt:
        print("Stopping notification pesistence")
