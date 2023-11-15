from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]


class Room(Base):
    __tablename__ = "Room"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    capacity: Mapped[int]

    devices: Mapped[List["IoTDevice"]] = relationship(back_populates="room")
    measurements: Mapped[List["NoiseMeasurement"]] = relationship(back_populates="room")


class IoTDevice(Base):
    __tablename__ = "IoTDevice"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("Room.id"))

    room: Mapped["Room"] = relationship(back_populates="devices")
    measurements: Mapped[List["NoiseMeasurement"]] = relationship(back_populates="device")


class NoiseMeasurement(Base):
    __tablename__ = "NoiseMeasurement"

    id: Mapped[int] = mapped_column(primary_key=True)
    noise_value: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    room_id: Mapped[int] = mapped_column(ForeignKey("Room.id"))
    device_id: Mapped[int] = mapped_column(ForeignKey("IoTDevice.id"))

    room: Mapped["Room"] = relationship(back_populates="measurements")
    device: Mapped["IoTDevice"] = relationship(back_populates="measurements")


Index(None, NoiseMeasurement.room_id, NoiseMeasurement.created_at)
