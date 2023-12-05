from fastapi import APIRouter

from src.shared.auth import crud, schemas
from src.shared.auth.crud import LoggedUser
from src.shared.database.dependencies import DatabaseSession

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup/")
def signup(db: DatabaseSession, user: schemas.UserAuth):
    crud.signup(db, user)


@auth_router.post("/login/", response_model=schemas.UserResponse)
def login(db: DatabaseSession, user: schemas.UserAuth):
    user, token = crud.login(db, user)
    return schemas.UserResponse(token=token, email=user.email, id=user.id)


@auth_router.post("/me/")
def me(user: LoggedUser):
    return user.email
