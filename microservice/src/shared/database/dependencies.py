from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.shared.database.connection import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    else:
        db.commit()
    finally:
        db.close()


DatabaseSession = Annotated[Session, Depends(get_db)]
