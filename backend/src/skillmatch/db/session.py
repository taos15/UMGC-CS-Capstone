"""Shared engine/session setup; SQLite and create_all remain transitional.

See docs/technical_debt/architecture-migration.md for persistence follow-ups.
"""

from collections.abc import Iterator

from sqlmodel import Session, create_engine

from skillmatch.core.config import DATABASE_URL
from skillmatch.db.base import Base

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def get_db() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
