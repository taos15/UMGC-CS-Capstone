"""SQLite connection setup for the backend package.

Alpha uses SQLite instead of the Postgres target in the design spec so the
team can start persisting data now; SQLAlchemy keeps the swap to Postgres a
connection-string change (see docs/TEAM_WORKFLOW.md technical debt notes).

No migration tool (e.g. Alembic) is used for the alpha: init_db() creates
tables directly from the SQLModel metadata. Schema changes recreate tables
rather than migrate them in place - acceptable for alpha since there's no
production data to preserve, but call this out as technical debt if the
project continues past the prototype stage.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel as Base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./skillmatch.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
