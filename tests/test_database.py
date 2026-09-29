from sqlalchemy import text

from backend.database import SessionLocal, engine


def test_engine_connects() -> None:
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar() == 1


def test_get_db_session_is_usable() -> None:
    session = SessionLocal()
    try:
        assert session.execute(text("SELECT 1")).scalar() == 1
    finally:
        session.close()
