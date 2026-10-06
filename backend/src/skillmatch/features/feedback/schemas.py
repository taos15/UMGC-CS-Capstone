"""Section 6 feedback contract; supervisor decisions do not assign staff."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator


class Feedback(BaseModel):
    match_run_id: str
    user_id: str
    decision: Literal['SELECTED', 'NOT_SELECTED', 'DEFERRED']
    selected_employee_id: str | None = None
    rating: int | None = None
    comment: str | None = None
    created_at: datetime


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')

    decision: Literal['SELECTED', 'NOT_SELECTED', 'DEFERRED']
    selected_employee_id: str | None = None
    rating: int | None = None
    comment: str | None = None

    @model_validator(mode='after')
    def validate_selection(self) -> 'FeedbackRequest':
        if self.decision == 'SELECTED' and not self.selected_employee_id:
            raise ValueError('SELECTED requires selected_employee_id.')
        if self.decision != 'SELECTED' and self.selected_employee_id is not None:
            raise ValueError('selected_employee_id is only valid for SELECTED.')
        return self
