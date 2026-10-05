"""Persistence operations for stored match runs (DB-002)."""

from datetime import timezone

from sqlmodel import Session, select

from skillmatch.features.recommendations.models import CandidateResult, MatchRun
from skillmatch.features.matching.schemas import CandidateResult as ResultSchema
from skillmatch.features.recommendations.schemas import MatchRun as RunSchema


def create_match_run(
    session: Session,
    *,
    job_id: str,
    requested_by: str,
    model_version: str,
    snapshot_hash: str,
    options: dict,
    results: list[dict],
) -> MatchRun:
    match_run = MatchRun(
        job_id=job_id,
        requested_by=requested_by,
        model_version=model_version,
        snapshot_hash=snapshot_hash,
        options=options,
    )
    session.add(match_run)
    session.flush()

    for result in results:
        session.add(CandidateResult(match_run_id=match_run.match_run_id, **result))

    session.commit()
    session.refresh(match_run)
    return match_run


def get_match_run(session: Session, match_run_id: str) -> MatchRun | None:
    return session.get(MatchRun, match_run_id)


def get_candidate_results(session: Session, match_run_id: str) -> list[CandidateResult]:
    statement = (
        select(CandidateResult)
        .where(CandidateResult.match_run_id == match_run_id)
        .order_by(CandidateResult.rank)
    )
    return list(session.exec(statement))


def build_match_run_snapshot(session: Session, match_run: MatchRun) -> RunSchema:
    """Serialize persisted facts only; the caller must authorize the run first."""
    options = match_run.options
    # REC-001 stored request aliases; expose the established shared DTO vocabulary.
    if 'max_results' not in options:
        options = {
            'max_results': options['topK'],
            'minimum_score': options['minimumScore'],
            'include_ineligible': options.get('includeIneligible', False),
        }
    generated_at = match_run.generated_at
    if generated_at.tzinfo is None:
        # SQLite drops timezone information from UTC persistence timestamps.
        generated_at = generated_at.replace(tzinfo=timezone.utc)
    return RunSchema(
        match_run_id=match_run.match_run_id,
        job_id=match_run.job_id,
        requested_by=match_run.requested_by,
        model_version=match_run.model_version,
        snapshot_hash=match_run.snapshot_hash,
        options=options,
        generated_at=generated_at.astimezone(timezone.utc),
        results=[ResultSchema.model_validate(row.model_dump())
                 for row in get_candidate_results(session, match_run.match_run_id)],
    )
