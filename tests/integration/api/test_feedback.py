"""Supervisor feedback is persistent audit evidence, never an assignment."""

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from skillmatch.db.session import get_db
from skillmatch.features.feedback.repository import get_feedback_for_match_run
from skillmatch.features.recommendations.repository import create_match_run
from skillmatch.main import app


@pytest.fixture
def feedback_run(client, local_test_account):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        run = create_match_run(
            session, job_id='historical-job', requested_by=local_test_account[2],
            model_version='historical-model', snapshot_hash='historical-hash',
            options={'max_results': 5, 'minimum_score': 0, 'include_ineligible': True},
            results=[{
                'rank': rank, 'employee_id': employee_id, 'score': 90,
                'eligible': eligible, 'component_scores': {'required_skills': .9},
                'matched_skills': ['stored-skill'], 'missing_skills': [],
                'matched_certifications': [], 'missing_certifications': [],
                'ineligible_reasons': [] if eligible else ['missing certification'],
                'explanation': 'Stored explanation.',
            } for rank, employee_id, eligible in [(1, 'eligible-employee', True), (2, 'ineligible-employee', False)]],
        )
        run_id = run.match_run_id
    def isolated_db():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_db] = isolated_db
    try:
        yield run_id, engine
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


@pytest.mark.parametrize('decision', ['SELECTED', 'NOT_SELECTED', 'DEFERRED'])
def test_feedback_records_authenticated_caller_and_preserves_run(client, feedback_run, local_test_account, decision, monkeypatch):
    run_id, engine = feedback_run
    before = client.get(f'/api/v1/match-runs/{run_id}').json()
    def forbidden(*args, **kwargs):
        pytest.fail('Feedback must not load live profiles or invoke matching/assignment')
    monkeypatch.setattr('skillmatch.features.recommendations.router.generate_recommendations', forbidden)
    monkeypatch.setattr('skillmatch.features.recommendations.service.get_employees', forbidden)
    body = {'decision': decision, 'rating': 5, 'comment': 'Human decision.'}
    if decision == 'SELECTED':
        body['selected_employee_id'] = 'eligible-employee'
    response = client.post(f'/api/v1/match-runs/{run_id}/feedback', json=body)
    assert response.status_code == 201
    saved = response.json()
    assert saved['match_run_id'] == run_id
    assert saved['user_id'] == local_test_account[2]
    assert saved['decision'] == decision
    assert saved['selected_employee_id'] == body.get('selected_employee_id')
    assert saved['created_at'].endswith('Z')
    assert saved['rating'] == 5 and saved['comment'] == 'Human decision.'
    assert response.headers['x-request-id']
    with Session(engine) as session:
        rows = get_feedback_for_match_run(session, run_id)
        assert len(rows) == 1
        assert rows[0].decision == decision and rows[0].user_id == local_test_account[2]
    assert client.get(f'/api/v1/match-runs/{run_id}').json() == before


@pytest.mark.parametrize('body', [
    {'decision': 'UNKNOWN'}, {'decision': 'SELECTED'},
    {'decision': 'DEFERRED', 'selected_employee_id': 'eligible-employee'},
    {'decision': 'NOT_SELECTED', 'selected_employee_id': 'eligible-employee'},
])
def test_invalid_decision_fields_never_persist(client, feedback_run, body):
    run_id, engine = feedback_run
    response = client.post(f'/api/v1/match-runs/{run_id}/feedback', json=body)
    assert response.status_code == 422
    assert response.json()['code'] == 'VALIDATION_ERROR'
    with Session(engine) as session:
        assert get_feedback_for_match_run(session, run_id) == []


@pytest.mark.parametrize('employee_id', ['not-in-run', 'ineligible-employee'])
def test_selected_employee_must_be_eligible_in_stored_run(client, feedback_run, employee_id):
    run_id, engine = feedback_run
    response = client.post(f'/api/v1/match-runs/{run_id}/feedback', json={
        'decision': 'SELECTED', 'selected_employee_id': employee_id,
    })
    assert response.status_code == 409
    assert response.json()['code'] == 'FEEDBACK_CONFLICT'
    with Session(engine) as session:
        assert get_feedback_for_match_run(session, run_id) == []


def test_viewer_is_rejected_before_protected_database_access(client, monkeypatch, local_test_account):
    import json
    password, _, user_id, encoded = local_test_account
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps({'viewer': {
        'user_id': user_id, 'role': 'VIEWER', 'password_hash': encoded,
    }}))
    token = client.post('/api/v1/auth/login', json={'username': 'viewer', 'password': password}).json()['access_token']
    def forbidden():
        pytest.fail('VIEWER accessed feedback persistence')
        yield
    app.dependency_overrides[get_db] = forbidden
    try:
        response = client.post('/api/v1/match-runs/any/feedback', json={'decision': 'DEFERRED'},
                               headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 403
        assert response.json()['code'] == 'FORBIDDEN'
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.mark.parametrize('role,owns_run,expected', [('ADMIN', False, 201), ('SUPERVISOR', True, 201), ('SUPERVISOR', False, 403)])
def test_feedback_enforces_run_scope(client, feedback_run, local_test_account, monkeypatch, role, owns_run, expected):
    import json
    from uuid import uuid4
    run_id, engine = feedback_run
    password, _, owner_id, encoded = local_test_account
    user_id = owner_id if owns_run else str(uuid4())
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps({'caller': {
        'user_id': user_id, 'role': role, 'password_hash': encoded,
    }}))
    token = client.post('/api/v1/auth/login', json={'username': 'caller', 'password': password}).json()['access_token']
    if expected == 403:
        def forbidden(*args, **kwargs):
            pytest.fail('Out-of-scope feedback accessed candidate evidence or persisted a decision')
        monkeypatch.setattr('skillmatch.features.feedback.service.get_candidate_results', forbidden)
        monkeypatch.setattr('skillmatch.features.feedback.service.create_feedback', forbidden)
    response = client.post(f'/api/v1/match-runs/{run_id}/feedback', json={
        'decision': 'SELECTED', 'selected_employee_id': 'eligible-employee',
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == expected
    with Session(engine) as session:
        rows = get_feedback_for_match_run(session, run_id)
        assert len(rows) == (1 if expected == 201 else 0)
    if expected == 201:
        assert response.json()['user_id'] == user_id
    else:
        assert response.json()['code'] == 'FORBIDDEN'
        assert 'eligible-employee' not in response.text
        assert owner_id not in response.text


def test_feedback_is_append_only_audit_history(client, feedback_run):
    run_id, engine = feedback_run
    for decision in ['DEFERRED', 'SELECTED', 'SELECTED']:
        body = {'decision': decision}
        if decision == 'SELECTED':
            body['selected_employee_id'] = 'eligible-employee'
        assert client.post(f'/api/v1/match-runs/{run_id}/feedback', json=body).status_code == 201
    with Session(engine) as session:
        rows = get_feedback_for_match_run(session, run_id)
        assert len({row.id for row in rows}) == 3
        assert sorted(row.decision for row in rows) == ['DEFERRED', 'SELECTED', 'SELECTED']


def test_missing_run_uses_canonical_error(client, feedback_run):
    _, engine = feedback_run
    response = client.post('/api/v1/match-runs/missing/feedback', json={'decision': 'DEFERRED'})
    assert response.status_code == 404
    assert response.json()['code'] == 'MATCH_RUN_NOT_FOUND'
    assert response.json()['request_id'] == response.headers['x-request-id']
    assert response.headers['content-type'] == 'application/problem+json'


@pytest.mark.parametrize('field', ['match_run_id', 'user_id', 'created_at'])
def test_client_cannot_spoof_audit_identity(client, feedback_run, field):
    run_id, engine = feedback_run
    response = client.post(f'/api/v1/match-runs/{run_id}/feedback', json={'decision': 'DEFERRED', field: 'spoofed'})
    assert response.status_code == 422
    assert response.json()['code'] == 'VALIDATION_ERROR'
    with Session(engine) as session:
        assert get_feedback_for_match_run(session, run_id) == []


@pytest.mark.parametrize('failure_point', ['get_match_run', 'get_candidate_results', 'create_feedback'])
def test_feedback_database_failures_are_safe(client, feedback_run, monkeypatch, failure_point):
    from sqlalchemy.exc import OperationalError
    run_id, engine = feedback_run
    def failed(*args, **kwargs):
        raise OperationalError('private SQL', {}, Exception('private database details'))
    monkeypatch.setattr(f'skillmatch.features.feedback.service.{failure_point}', failed)
    response = client.post(f'/api/v1/match-runs/{run_id}/feedback', json={
        'decision': 'SELECTED', 'selected_employee_id': 'eligible-employee',
    })
    assert response.status_code == 503
    assert response.json()['code'] == 'DATABASE_UNAVAILABLE'
    assert 'private' not in response.text
    assert response.json()['request_id'] == response.headers['x-request-id']
    with Session(engine) as session:
        assert get_feedback_for_match_run(session, run_id) == []
