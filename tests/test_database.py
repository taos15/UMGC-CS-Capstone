from sqlmodel import Session, text

from backend.database import engine, init_db


def test_engine_connects() -> None:
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar() == 1


def test_init_db_runs_cleanly() -> None:
    init_db()


def test_get_db_session_is_usable() -> None:
    with Session(engine) as session:
        assert session.execute(text("SELECT 1")).scalar() == 1
