import time
from functools import cmp_to_key

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, delete, case, func, text
from starlette import status

from src.auth.crud import LoggedUser
from src.database import models
from src.database.database import DatabaseSession
from src.iot import schemas, crud

iot_router = APIRouter(tags=["IoT"])


def compare_int(a: int, b: int):
    if a < b:
        return -1
    elif a == b:
        return 0
    return 1


def compare_rooms(a: schemas.Room, b: schemas.Room):
    if (a.editable and b.editable) or (not a.editable and not b.editable):
        return compare_int(a.id, b.id)
    return -1 if a.editable else 1


@iot_router.post("/rooms/")
def create_room(db: DatabaseSession, user: LoggedUser, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, creator_id=user.id)
    db.add(db_room)


@iot_router.get(
    "/rooms/",
    summary="Get all the rooms that the current user is subscribed to",
    response_model=list[schemas.Room],
)
def get_subscribed_rooms(db: DatabaseSession, user: LoggedUser):
    return crud.get_subscribed_rooms(db, user)


@iot_router.get(
    "/rooms/{room_id}/",
    summary="Get all the devices that are asigned to the room",
    response_model=list[schemas.Device],
)
def get_room_devices(db: DatabaseSession, user: LoggedUser, room_id: int):
    return db.scalars(select(models.Device).filter_by(room_id=room_id)).all()


@iot_router.post("/rooms/{room_id}/subscription/")
def subscribe_to_room(db: DatabaseSession, user: LoggedUser, room_id: int):
    crud.subscribe_to_room(db, user, room_id)


@iot_router.delete("/rooms/{room_id}/subscription/")
def unsubscribe_from_room(db: DatabaseSession, user: LoggedUser, room_id: int):
    db.execute(
        delete(models.RoomSubscription).filter_by(user_id=user.id, room_id=room_id)
    )
