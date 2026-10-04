from sqlmodel import text

from skillmatch.db.session import engine, get_db, init_db


def test_engine_connects() -> None:
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar() == 1


def test_init_db_runs_cleanly() -> None:
    init_db()


def test_get_db_session_is_usable() -> None:
    sessions = get_db()
    session = next(sessions)
    try:
        assert session.execute(text("SELECT 1")).scalar() == 1
    finally:
        sessions.close()
