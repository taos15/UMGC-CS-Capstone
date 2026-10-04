"""Persistence model for supervisor feedback (DB-002).

Feedback validation and HTTP wiring are a separate story; feedback never
updates the live matching model automatically.
"""

import uuid
from datetime import datetime, timezone

from sqlmodel import Field

from skillmatch.db.base import Base


def _new_id() -> str:
    return uuid.uuid4().hex


class Feedback(Base, table=True):
    id: str = Field(default_factory=_new_id, primary_key=True)
    match_run_id: str = Field(foreign_key="matchrun.match_run_id", index=True)
    user_id: str
    decision: str
    selected_employee_id: str | None = None
    rating: int | None = None
    comment: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
