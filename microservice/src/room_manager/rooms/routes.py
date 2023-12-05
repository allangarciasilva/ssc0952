from fastapi import APIRouter
from sqlalchemy import select, delete

from src.room_manager.rooms import schemas, crud
from src.shared.auth.crud import LoggedUser
from src.shared.database import models
from src.shared.database.dependencies import DatabaseSession

rooms_router = APIRouter(tags=["Rooms"], prefix="/rooms")


@rooms_router.post("/")
def create_room(db: DatabaseSession, user: LoggedUser, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, creator_id=user.id)
    db.add(db_room)


@rooms_router.get(
    "/",
    summary="Get all the rooms that the current user is subscribed to",
    response_model=list[schemas.Room],
)
def get_subscribed_rooms(db: DatabaseSession, user: LoggedUser):
    return crud.get_subscribed_rooms(db, user)


@rooms_router.get(
    "/{room_id}/",
    summary="Get all the devices that are asigned to the room",
    response_model=list[schemas.Device],
)
def get_room_devices(db: DatabaseSession, user: LoggedUser, room_id: int):
    return db.scalars(select(models.Device).filter_by(room_id=room_id)).all()


@rooms_router.post("/{room_id}/subscription/")
def subscribe_to_room(db: DatabaseSession, user: LoggedUser, room_id: int):
    crud.subscribe_to_room(db, user, room_id)


@rooms_router.delete("/{room_id}/subscription/")
def unsubscribe_from_room(db: DatabaseSession, user: LoggedUser, room_id: int):
    db.execute(
        delete(models.RoomSubscription).filter_by(user_id=user.id, room_id=room_id)
    )


@rooms_router.get("/{room_id}/measurements/{device_id}/")
def get_historical_data(
        db: DatabaseSession,
        user: LoggedUser,
        room_id: int,
        device_id: int,
        search_filter: schemas.MeasurementFilter,
):
    return db.scalars(
        select(models.NoiseMeasurement)
        .where(models.NoiseMeasurement.device_id == device_id)
        .where(models.NoiseMeasurement.room_id == room_id)
        .where(models.NoiseMeasurement.created_at >= search_filter.dt_min)
        .where(models.NoiseMeasurement.created_at <= search_filter.dt_max)
    ).all()
