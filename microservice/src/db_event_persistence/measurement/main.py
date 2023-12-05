import traceback

import orjson
import uvloop
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session

from src.shared.database import models
from src.shared.database.connection import SessionLocal
from src.shared.settings import SETTINGS


def persist_measurement(db: Session, device_name: str, noise_value: float):
    db_device = db.query(models.Device).filter_by(name=device_name).first()
    if not db_device:
        return

    db_measurement = models.NoiseMeasurement(
        noise_value=noise_value,
        room_id=db_device.room_id,
        device_id=db_device.id
    )

    db.add(db_measurement)
    db.commit()


async def listen_to_measurements():
    db = SessionLocal()
    consumer = AIOKafkaConsumer('noise', bootstrap_servers=SETTINGS.kafka_server, group_id="measurement-consumer")
    await consumer.start()

    try:
        async for msg in consumer:
            try:
                persist_measurement(db, msg.key.decode(), orjson.loads(msg.value))
            except Exception:
                traceback.print_exc()
    finally:
        await consumer.stop()


if __name__ == "__main__":
    print("Starting measurement pesistence")
    try:
        uvloop.run(listen_to_measurements())
    except KeyboardInterrupt:
        print("Stopping measurement pesistence")
