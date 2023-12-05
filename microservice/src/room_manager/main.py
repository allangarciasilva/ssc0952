from fastapi import FastAPI

from src.room_manager.auth import auth_router
from src.room_manager.rooms.routes import rooms_router
from src.shared.database.models import create_all_tables
from src.shared.utils import run_app

app = FastAPI()
app.include_router(auth_router)
app.include_router(rooms_router)

if __name__ == "__main__":
    create_all_tables()
    run_app("src.room_manager.main:app", 8080)
