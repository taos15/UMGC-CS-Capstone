"""REC-002: historical run retrieval returns persisted evidence, without matching."""

from datetime import datetime, timezone

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from skillmatch.db.session import get_db
from skillmatch.features.recommendations.repository import create_match_run
from skillmatch.main import app


@pytest.fixture
def stored_run(client, local_test_account):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        run = create_match_run(
            session, job_id='historical-job', requested_by=local_test_account[2],
            model_version='historical-model', snapshot_hash='historical-hash',
            options={'topK': 3, 'minimumScore': 10, 'includeIneligible': False, 'includeMissingSkills': True},
            results=[{
                'rank': rank, 'employee_id': f'historical-employee-{rank}', 'score': score,
                'eligible': True, 'component_scores': {'required_skills': .9},
                'matched_skills': ['stored-skill'], 'missing_skills': ['stored-gap'],
                'matched_certifications': ['stored-certificate'], 'missing_certifications': [],
                'ineligible_reasons': [], 'explanation': 'Stored explanation.',
            } for rank, score in [(2, 60), (1, 90)]],
        )
        run.generated_at = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        session.add(run); session.commit(); session.refresh(run)
        run_id = run.match_run_id
    def isolated_db():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_db] = isolated_db
    try:
        yield run_id
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def test_get_returns_complete_stored_run_without_recomputing(client, stored_run, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('Historical retrieval must not load live profiles or invoke matching')
    monkeypatch.setattr('skillmatch.features.recommendations.router.get_job', forbidden)
    monkeypatch.setattr('skillmatch.features.recommendations.router.generate_recommendations', forbidden)
    monkeypatch.setattr('skillmatch.features.recommendations.service.get_employees', forbidden)
    response = client.get(f'/api/v1/match-runs/{stored_run}')
    assert response.status_code == 200
    body = response.json()
    assert body['match_run_id'] == stored_run
    assert body['job_id'] == 'historical-job'
    assert body['model_version'] == 'historical-model'
    assert body['snapshot_hash'] == 'historical-hash'
    assert body['generated_at'] == '2026-01-02T03:04:05Z'
    assert body['options'] == {'max_results': 3, 'minimum_score': 10, 'include_ineligible': False}
    assert [item['rank'] for item in body['results']] == [1, 2]
    assert body['results'][0] == {
        'rank': 1, 'employee_id': 'historical-employee-1', 'score': 90,
        'eligible': True, 'component_scores': {'required_skills': .9},
        'matched_skills': ['stored-skill'], 'missing_skills': ['stored-gap'],
        'matched_certifications': ['stored-certificate'], 'missing_certifications': [],
        'ineligible_reasons': [], 'explanation': 'Stored explanation.',
    }
    assert response.headers['x-request-id']
    again = client.get(f'/api/v1/match-runs/{stored_run}')
    assert again.json() == body


def test_unknown_match_run_returns_typed_404(client, stored_run):
    response = client.get('/api/v1/match-runs/missing')
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/problem+json'
    assert response.json()['code'] == 'MATCH_RUN_NOT_FOUND'
    assert response.json()['request_id'] == response.headers['x-request-id']


def test_unauthenticated_retrieval_never_accesses_database(client, monkeypatch):
    def forbidden():
        pytest.fail('Unauthenticated request accessed protected persistence')
        yield
    app.dependency_overrides[get_db] = forbidden
    try:
        response = client.get('/api/v1/match-runs/any', headers={'Authorization': ''})
        assert response.status_code == 401
        assert response.json()['code'] == 'AUTH_REQUIRED'
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.mark.parametrize('role', ['ADMIN', 'SUPERVISOR', 'VIEWER'])
@pytest.mark.parametrize('owns_run', [True, False])
def test_match_run_scope_uses_authenticated_requester(client, stored_run, monkeypatch, role, owns_run):
    import json
    from uuid import uuid4
    from skillmatch.features.auth.repository import get_auth_settings

    # Real login/token validation, not an override of authorization dependencies.
    from skillmatch.core.security import hash_password
    password = 'test-scope-password'
    owner_id = next(iter(get_auth_settings().users.values())).user_id
    user_id = str(owner_id if owns_run else uuid4())
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps({'scope-user': {
        'user_id': user_id, 'role': role, 'password_hash': hash_password(password),
    }}))
    token = client.post('/api/v1/auth/login', json={'username': 'scope-user', 'password': password}).json()['access_token']
    if not owns_run and role != 'ADMIN':
        def forbidden(*args, **kwargs):
            pytest.fail('Out-of-scope request loaded protected candidate evidence')
        monkeypatch.setattr('skillmatch.features.recommendations.router.build_match_run_snapshot', forbidden)
    response = client.get(f'/api/v1/match-runs/{stored_run}', headers={'Authorization': f'Bearer {token}'})
    if owns_run or role == 'ADMIN':
        assert response.status_code == 200
        assert response.json()['requested_by'] == str(owner_id)
    else:
        assert response.status_code == 403
        assert response.json()['code'] == 'FORBIDDEN'
        assert response.json()['detail'] == 'You do not have permission to perform this action.'
        assert response.json()['request_id'] == response.headers['x-request-id']
        assert 'historical' not in response.text
        assert str(owner_id) not in response.text


def test_database_failure_returns_safe_503(client, stored_run, monkeypatch):
    from sqlalchemy.exc import OperationalError
    def broken(*args, **kwargs):
        raise OperationalError('private SQL', {}, Exception('private database credentials'))
    monkeypatch.setattr('skillmatch.features.recommendations.router.get_match_run', broken)
    response = client.get(f'/api/v1/match-runs/{stored_run}')
    assert response.status_code == 503
    assert response.json()['code'] == 'DATABASE_UNAVAILABLE'
    assert 'private' not in response.text
    assert response.json()['request_id'] == response.headers['x-request-id']


def test_new_recommendation_can_be_retrieved_as_the_same_snapshot(client, stored_run):
    created = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    assert created.status_code == 200
    original = created.json()
    response = client.get(f"/api/v1/match-runs/{original['match_run_id']}")
    assert response.status_code == 200
    assert response.json()['results'] == original['recommendations']
    assert response.json()['model_version'] == original['model_version']
