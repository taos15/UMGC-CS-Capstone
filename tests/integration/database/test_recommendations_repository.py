from sqlmodel import Session, SQLModel, create_engine

from skillmatch.features.recommendations.repository import (
    create_match_run,
    get_candidate_results,
    get_match_run,
)


def _session() -> Session:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_create_match_run_persists_run_and_candidate_results() -> None:
    with _session() as session:
        match_run = create_match_run(
            session,
            job_id="job-electrician",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="abc123",
            options={"topK": 5, "minimumScore": 0.0},
            results=[
                {
                    "rank": 1,
                    "employee_id": "emp-alex",
                    "score": 95.0,
                    "eligible": True,
                    "component_scores": {"required_skills": 55.0},
                    "matched_skills": ["electrical wiring"],
                    "missing_skills": [],
                    "matched_certifications": ["licensed electrician"],
                    "missing_certifications": [],
                    "ineligible_reasons": [],
                    "explanation": "Strong match.",
                },
                {
                    "rank": 2,
                    "employee_id": "emp-jordan",
                    "score": 70.0,
                    "eligible": True,
                    "component_scores": {"required_skills": 40.0},
                    "matched_skills": ["electrical wiring"],
                    "missing_skills": ["blueprint reading"],
                    "matched_certifications": [],
                    "missing_certifications": ["licensed electrician"],
                    "ineligible_reasons": [],
                    "explanation": "Partial match.",
                },
            ],
        )

        assert match_run.match_run_id
        assert match_run.job_id == "job-electrician"
        assert match_run.options == {"topK": 5, "minimumScore": 0.0}

        results = get_candidate_results(session, match_run.match_run_id)
        assert [result.rank for result in results] == [1, 2]
        assert results[0].employee_id == "emp-alex"
        assert results[0].matched_certifications == ["licensed electrician"]


def test_get_match_run_returns_immutable_stored_run() -> None:
    with _session() as session:
        created = create_match_run(
            session,
            job_id="job-hvac",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="def456",
            options={},
            results=[],
        )

        fetched = get_match_run(session, created.match_run_id)

        assert fetched is not None
        assert fetched.match_run_id == created.match_run_id
        assert fetched.job_id == "job-hvac"


def test_get_match_run_returns_none_when_missing() -> None:
    with _session() as session:
        assert get_match_run(session, "does-not-exist") is None


def test_snapshot_serializes_legacy_options_without_mutating_persistence() -> None:
    from skillmatch.features.recommendations.repository import build_match_run_snapshot
    with _session() as session:
        options = {'topK': 4, 'minimumScore': 20, 'includeIneligible': True, 'includeMissingSkills': False}
        created = create_match_run(
            session, job_id='historical-job', requested_by='user', model_version='historical-model',
            snapshot_hash='stored-hash', options=options, results=[],
        )
        snapshot = build_match_run_snapshot(session, created)
        assert snapshot.options.model_dump() == {
            'max_results': 4, 'minimum_score': 20, 'include_ineligible': True,
        }
        assert snapshot.results == []
        assert snapshot.generated_at.utcoffset().total_seconds() == 0
        assert created.options == options


def test_snapshot_accepts_canonical_options() -> None:
    from skillmatch.features.recommendations.repository import build_match_run_snapshot
    with _session() as session:
        options = {'max_results': 4, 'minimum_score': 20, 'include_ineligible': False}
        created = create_match_run(
            session, job_id='historical-job', requested_by='user', model_version='historical-model',
            snapshot_hash='stored-hash', options=options, results=[],
        )
        assert build_match_run_snapshot(session, created).options.model_dump() == options


def _stored_candidate(rank=1):
    return {
        'rank': rank, 'employee_id': f'employee-{rank}', 'score': 62.5, 'eligible': False,
        'component_scores': {'required_skills': 0.5, 'preferred_skills': 1.0,
                             'required_certifications': 0.0, 'experience': 1.0},
        'matched_skills': ['wiring'], 'missing_skills': ['blueprints'],
        'matched_certifications': [], 'missing_certifications': ['license'],
        'ineligible_reasons': ['MISSING_MANDATORY_CERTIFICATION:license'],
        'explanation': 'Missing mandatory license; supervisor review required.',
    }


def _persist_run(session, results):
    return create_match_run(
        session, job_id='job', requested_by='supervisor',
        model_version='rpce-55-20-15-10-v1', snapshot_hash='fixed-snapshot',
        options={'max_results': 5, 'minimum_score': 0, 'include_ineligible': True},
        results=results,
    )


def test_snapshot_survives_database_reopen_and_returned_dto_mutation(tmp_path):
    from skillmatch.features.recommendations.repository import build_match_run_snapshot

    database_url = f"sqlite:///{tmp_path / 'match-runs.db'}"
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        created = _persist_run(session, [_stored_candidate(2), _stored_candidate(1)])
        original = build_match_run_snapshot(session, created).model_dump(mode='json')
    engine.dispose()

    reopened = create_engine(database_url)
    try:
        with Session(reopened) as session:
            stored = get_match_run(session, created.match_run_id)
            assert stored is not None
            snapshot = build_match_run_snapshot(session, stored)
            assert snapshot.model_dump(mode='json') == original
            assert [result.model_dump() for result in snapshot.results] == [
                _stored_candidate(1), _stored_candidate(2),
            ]
            assert snapshot.job_id == 'job'
            assert snapshot.requested_by == 'supervisor'
            assert snapshot.model_version == 'rpce-55-20-15-10-v1'
            assert snapshot.snapshot_hash == 'fixed-snapshot'
            snapshot.results[0].matched_skills.append('changed')
            snapshot.options.max_results = 1
            assert build_match_run_snapshot(session, stored).model_dump(mode='json') == original
    finally:
        reopened.dispose()


def test_failed_candidate_insert_rolls_back_run_and_session_can_be_reused():
    import pytest
    from sqlalchemy.exc import IntegrityError
    from sqlmodel import select
    from skillmatch.features.recommendations.models import CandidateResult, MatchRun

    with _session() as session:
        existing = _persist_run(session, [_stored_candidate()])
        # A real NOT NULL constraint failure occurs after the parent run is flushed.
        invalid = _stored_candidate(2)
        invalid['employee_id'] = None
        with pytest.raises(IntegrityError):
            _persist_run(session, [_stored_candidate(), invalid])
        assert [row.match_run_id for row in session.exec(select(MatchRun))] == [existing.match_run_id]
        assert [row.match_run_id for row in session.exec(select(CandidateResult))] == [existing.match_run_id]
        recovered = _persist_run(session, [_stored_candidate()])
        assert recovered.match_run_id != existing.match_run_id
        assert len(list(session.exec(select(MatchRun)))) == 2
        assert len(list(session.exec(select(CandidateResult)))) == 2
