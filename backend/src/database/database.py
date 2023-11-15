from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker

from src.settings import SETTINGS

engine = create_engine(SETTINGS.sqlalchemy_url)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def create_all_tables(drop=False):
    if drop:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
