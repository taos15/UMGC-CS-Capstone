"""SQLite connection setup for the backend package.

Alpha uses SQLite instead of the Postgres target in the design spec so the
team can start persisting data now; SQLAlchemy keeps the swap to Postgres a
connection-string change (see docs/TEAM_WORKFLOW.md technical debt notes).
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./skillmatch.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
