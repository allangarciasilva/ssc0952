import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.auth.crud import LoggedUser, LoggedUserWs
from src.auth.routes import auth_router
from src.connection import connection_manager
from src.database import create_all_tables
from src.database.database import DatabaseSession
from src.iot import crud
from src.iot.mqtt import setup_mqtt, shutdown_mqtt
from src.iot.routes import iot_router

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Start up
    create_all_tables(drop=False)
    setup_mqtt()

    yield

    # Shutdown
    shutdown_mqtt()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(iot_router)


@app.websocket("/ws/user/")
async def websocket_subscribe_to_device(user: LoggedUserWs, ws: WebSocket):
    await ws.accept()
    connection_manager.subscribe(ws, f"user/{user.id}")
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        connection_manager.unsubscribe(ws, f"user/{user.id}")


@app.websocket("/ws/noise/{device_name}")
async def websocket_subscribe_to_device(
    device_name: str,
    ws: WebSocket,
    user: LoggedUserWs,
):
    await ws.accept()
    connection_manager.subscribe(ws, f"noise/{device_name}")
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        connection_manager.unsubscribe(ws, f"noise/{device_name}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
