from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.shared.settings import SETTINGS

engine = create_engine(SETTINGS.sqlalchemy_url, echo=SETTINGS.debug)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
