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
    # Local imports: registers each persistent feature's tables on Base.metadata
    # before create_all runs, without db/ importing every feature at module load.
    from skillmatch.features.feedback import models as _feedback_models  # noqa: F401
    from skillmatch.features.recommendations import (  # noqa: F401
        models as _recommendations_models,
    )

    from skillmatch.features.employees import models as _employee_models  # noqa: F401
    from skillmatch.features.jobs import models as _job_models  # noqa: F401

    from skillmatch.features.skills import models as _skill_models  # noqa: F401

    if engine.dialect.name == 'sqlite':
        Base.metadata.create_all(bind=engine)
    else:
        # PostgreSQL schema creation is an explicit Alembic deployment step.
        with engine.connect() as connection:
            from sqlalchemy import text
            connection.execute(text('SELECT 1'))
