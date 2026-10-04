"""Section 6 feedback contract; supervisor decisions do not assign staff."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Feedback(BaseModel):
    match_run_id: str
    user_id: str
    decision: Literal['SELECTED', 'NOT_SELECTED', 'DEFERRED']
    selected_employee_id: str | None = None
    rating: int | None = None
    comment: str | None = None
    created_at: datetime
