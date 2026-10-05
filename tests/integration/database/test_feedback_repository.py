from sqlmodel import Session, SQLModel, create_engine

from skillmatch.features.feedback.repository import (
    create_feedback,
    get_feedback_for_match_run,
)
from skillmatch.features.recommendations.repository import create_match_run


def _session() -> Session:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_create_feedback_persists_decision_against_match_run() -> None:
    with _session() as session:
        match_run = create_match_run(
            session,
            job_id="job-electrician",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="abc123",
            options={},
            results=[],
        )

        feedback = create_feedback(
            session,
            match_run_id=match_run.match_run_id,
            user_id="supervisor-1",
            decision="SELECTED",
            selected_employee_id="emp-alex",
            rating=5,
            comment="Great fit.",
        )

        assert feedback.id
        assert feedback.match_run_id == match_run.match_run_id
        assert feedback.decision == "SELECTED"
        assert feedback.selected_employee_id == "emp-alex"


def test_get_feedback_for_match_run_returns_only_matching_rows() -> None:
    with _session() as session:
        run_a = create_match_run(
            session,
            job_id="job-electrician",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="abc123",
            options={},
            results=[],
        )
        run_b = create_match_run(
            session,
            job_id="job-hvac",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="def456",
            options={},
            results=[],
        )
        create_feedback(
            session,
            match_run_id=run_a.match_run_id,
            user_id="supervisor-1",
            decision="NOT_SELECTED",
        )
        create_feedback(
            session,
            match_run_id=run_b.match_run_id,
            user_id="supervisor-1",
            decision="DEFERRED",
        )

        feedback_for_a = get_feedback_for_match_run(session, run_a.match_run_id)

        assert len(feedback_for_a) == 1
        assert feedback_for_a[0].decision == "NOT_SELECTED"


def test_failed_feedback_commit_rolls_back_pending_audit_row(monkeypatch) -> None:
    import pytest
    from sqlalchemy.exc import OperationalError
    with _session() as session:
        run = create_match_run(
            session, job_id='job', requested_by='supervisor', model_version='v1',
            snapshot_hash='hash', options={}, results=[],
        )
        def failed_commit():
            raise OperationalError('INSERT feedback', {}, Exception('database unavailable'))
        monkeypatch.setattr(session, 'commit', failed_commit)
        with pytest.raises(OperationalError):
            create_feedback(session, match_run_id=run.match_run_id, user_id='supervisor', decision='DEFERRED')
        assert not session.new
        assert get_feedback_for_match_run(session, run.match_run_id) == []
