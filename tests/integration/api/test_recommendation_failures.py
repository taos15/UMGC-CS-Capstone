"""Failure paths must not leave partial runs or candidate evidence."""

import pytest
from sqlalchemy import event
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from skillmatch.db.session import get_db
from skillmatch.features.recommendations.models import MatchRun, CandidateResult
from skillmatch.main import app


@pytest.fixture
def isolated_database(client):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    sessions = []
    def database():
        with Session(engine) as session:
            sessions.append(session)
            yield session
    app.dependency_overrides[get_db] = database
    try:
        yield engine, sessions
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def assert_empty(engine):
    with Session(engine) as session:
        assert list(session.exec(select(MatchRun))) == []
        assert list(session.exec(select(CandidateResult))) == []


def assert_problem(response, status, code):
    assert response.status_code == status
    assert response.headers['content-type'] == 'application/problem+json'
    assert response.json()['code'] == code
    assert response.json()['request_id'] == response.headers['x-request-id']
    assert 'private' not in response.text


@pytest.mark.parametrize('stage', ['evaluate_eligibility', 'score_candidate', 'rank_candidates', 'build_candidate_result'])
def test_engine_failure_is_503_and_never_persists(client, isolated_database, monkeypatch, stage):
    engine, _ = isolated_database
    def failed(*args, **kwargs):
        raise RuntimeError('private engine internals')
    monkeypatch.setattr(f'skillmatch.features.recommendations.service.{stage}', failed)
    response = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    assert_problem(response, 503, 'MATCH_ENGINE_UNAVAILABLE')
    assert_empty(engine)


@pytest.mark.parametrize('stage', ['job', 'employees'])
def test_repository_read_failure_is_503(client, isolated_database, monkeypatch, stage):
    engine, _ = isolated_database
    def failed(*args, **kwargs):
        raise OperationalError('private SQL', {}, Exception('private database details'))
    target = 'router.get_job' if stage == 'job' else 'service.get_employees'
    monkeypatch.setattr(f'skillmatch.features.recommendations.{target}', failed)
    response = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    assert_problem(response, 503, 'DATABASE_UNAVAILABLE')
    assert_empty(engine)


def test_candidate_insert_failure_rolls_back_already_flushed_run(client, isolated_database):
    engine, _ = isolated_database
    def failed(mapper, connection, candidate):
        # The parent run has already been INSERTed when candidate persistence fails.
        assert connection.exec_driver_sql('SELECT COUNT(*) FROM matchrun').scalar() == 1
        raise OperationalError('private INSERT', {}, Exception('private database error'))
    event.listen(CandidateResult, 'before_insert', failed)
    try:
        response = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
        assert_problem(response, 503, 'DATABASE_UNAVAILABLE')
        assert_empty(engine)
    finally:
        event.remove(CandidateResult, 'before_insert', failed)
    # The next request can use the database normally after rollback.
    assert client.post('/api/v1/jobs/job-electrician/recommendations', json={}).status_code == 200


@pytest.mark.parametrize('payload', [{'top_k': 0}, {'minimum_score': 101}])
def test_request_validation_never_persists(client, isolated_database, payload):
    engine, _ = isolated_database
    response = client.post('/api/v1/jobs/job-electrician/recommendations', json=payload)
    assert_problem(response, 422, 'VALIDATION_ERROR')
    assert response.json()['field_errors']
    assert_empty(engine)


@pytest.mark.parametrize('event_name', ['after_insert', 'before_commit'])
def test_failure_after_candidate_rows_exist_rolls_back_everything(client, isolated_database, event_name):
    engine, _ = isolated_database
    def failed(*args):
        connection = args[1] if event_name == 'after_insert' else args[0].connection()
        assert connection.exec_driver_sql('SELECT COUNT(*) FROM matchrun').scalar() == 1
        assert connection.exec_driver_sql('SELECT COUNT(*) FROM candidateresult').scalar() > 0
        raise OperationalError('private SQL', {}, Exception('private transaction error'))
    target = CandidateResult if event_name == 'after_insert' else Session
    event.listen(target, event_name, failed)
    try:
        response = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
        assert_problem(response, 503, 'DATABASE_UNAVAILABLE')
        assert_empty(engine)
    finally:
        event.remove(target, event_name, failed)


@pytest.mark.parametrize('invalid_state,status,code', [
    ('CLOSED', 409, 'JOB_NOT_OPEN'), ('NO_CRITERIA', 422, 'JOB_HAS_NO_CRITERIA'),
])
def test_invalid_job_state_never_persists(client, isolated_database, monkeypatch, invalid_state, status, code):
    from skillmatch.features.jobs.seed import JOBS
    job = JOBS[0].model_copy(deep=True)
    if invalid_state == 'CLOSED':
        job.status = 'CLOSED'
    else:
        job.skill_requirement_details = []
        job.required_certifications = []
        job.minimum_years_experience = 0
    monkeypatch.setattr('skillmatch.features.recommendations.router.get_job', lambda _: job)
    response = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    assert_problem(response, status, code)
    assert_empty(isolated_database[0])
