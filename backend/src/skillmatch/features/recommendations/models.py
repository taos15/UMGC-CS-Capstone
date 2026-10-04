"""Persistence models for stored match runs (DB-002).

Recommendation HTTP/orchestration wiring that creates these rows from a live
request is a separate story; see docs/technical_debt/architecture-migration.md.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column
from sqlmodel import Field

from skillmatch.db.base import Base


def _new_id() -> str:
    return uuid.uuid4().hex


class MatchRun(Base, table=True):
    match_run_id: str = Field(default_factory=_new_id, primary_key=True)
    job_id: str
    requested_by: str
    model_version: str
    snapshot_hash: str
    options: dict = Field(default_factory=dict, sa_column=Column(JSON))
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CandidateResult(Base, table=True):
    id: str = Field(default_factory=_new_id, primary_key=True)
    match_run_id: str = Field(foreign_key="matchrun.match_run_id", index=True)
    rank: int
    employee_id: str
    score: float
    eligible: bool = True
    component_scores: dict = Field(default_factory=dict, sa_column=Column(JSON))
    matched_skills: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    missing_skills: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    matched_certifications: list[str] = Field(
        default_factory=list, sa_column=Column(JSON)
    )
    missing_certifications: list[str] = Field(
        default_factory=list, sa_column=Column(JSON)
    )
    ineligible_reasons: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    explanation: str = ""
