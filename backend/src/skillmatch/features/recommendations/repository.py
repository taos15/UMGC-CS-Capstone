"""Persistence operations for stored match runs (DB-002)."""

from sqlmodel import Session, select

from skillmatch.features.recommendations.models import CandidateResult, MatchRun


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
