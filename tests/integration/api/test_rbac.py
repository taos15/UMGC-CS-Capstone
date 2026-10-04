import json
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from skillmatch.main import app

ROLES = ('ADMIN', 'SUPERVISOR', 'VIEWER')
# Independent expectations from spec section 5, including stub success statuses.
MATRIX = [
    ('GET', '/api/v1/skills', ROLES, 501),
    ('POST', '/api/v1/skills', ('ADMIN',), 501),
    ('GET', '/api/v1/employees', ROLES, 200),
    ('POST', '/api/v1/employees', ('ADMIN',), 501),
    ('GET', '/api/v1/employees/emp-alex', ROLES, 200),
    ('PUT', '/api/v1/employees/emp-alex', ('ADMIN',), 501),
    ('GET', '/api/v1/jobs', ROLES, 501),
    ('POST', '/api/v1/jobs', ('ADMIN',), 501),
    ('GET', '/api/v1/jobs/job-electrician', ROLES, 200),
    ('PUT', '/api/v1/jobs/job-electrician', ('ADMIN',), 501),
    ('POST', '/api/v1/jobs/job-electrician/recommendations', ('ADMIN', 'SUPERVISOR'), 200),
    ('GET', '/api/v1/match-runs/run', ROLES, 501),
    ('POST', '/api/v1/match-runs/run/feedback', ('ADMIN', 'SUPERVISOR'), 501),
]


@pytest.fixture
def role_client(request, monkeypatch, local_test_account):
    password, secret, _, encoded = local_test_account
    accounts = {role.lower(): {'user_id': str(uuid4()), 'role': role, 'password_hash': encoded} for role in ROLES}
    monkeypatch.setenv('SKILLMATCH_JWT_SECRET', secret)
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps(accounts))
    with TestClient(app) as client:
        response = client.post('/api/v1/auth/login', json={'username': request.param.lower(), 'password': password})
        assert response.status_code == 200
        client.headers['Authorization'] = 'Bearer ' + response.json()['access_token']
        yield request.param, client


@pytest.mark.parametrize('role_client', ROLES, indirect=True)
@pytest.mark.parametrize('method,path,allowed,status', MATRIX)
def test_route_role_matrix(role_client, method, path, allowed, status):
    role, client = role_client
    response = client.request(method, path, json={} if method == 'POST' else None)
    assert response.status_code == (status if role in allowed else 403)
    if role not in allowed:
        assert response.headers['content-type'] == 'application/problem+json'
        assert response.json() == {
            'type': 'about:blank', 'title': 'Forbidden', 'status': 403,
            'code': 'FORBIDDEN', 'request_id': response.headers['x-request-id'],
            'detail': 'You do not have permission to perform this action.', 'field_errors': [],
        }
        assert 'www-authenticate' not in response.headers


@pytest.mark.parametrize('method,path,allowed,status', MATRIX)
@pytest.mark.parametrize('authorization', [None, 'Bearer invalid', 'Basic ignored'])
def test_missing_or_invalid_auth_is_401_on_every_workforce_route(method, path, allowed, status, authorization, client):
    # Override the fixture's legitimate token to exercise real authentication failures.
    headers = {'Authorization': authorization or ''}
    response = client.request(method, path, headers=headers, json={} if method == 'POST' else None)
    assert response.status_code == 401
    assert response.json()['code'] == 'AUTH_REQUIRED'
    assert response.json()['field_errors'] == []
    assert response.json()['detail'] == 'A valid bearer token is required.'
    assert response.json()['request_id'] == response.headers['x-request-id']
    assert response.headers['www-authenticate'] == 'Bearer'


@pytest.mark.parametrize('role_client', ['VIEWER'], indirect=True)
def test_forbidden_recommendation_never_accesses_job_or_candidates(role_client, monkeypatch):
    _, client = role_client
    def protected_call(*args, **kwargs):
        pytest.fail('Protected data was accessed before authorization')
    monkeypatch.setattr('skillmatch.features.recommendations.router.get_job', protected_call)
    monkeypatch.setattr('skillmatch.features.recommendations.router.recommend_employees', protected_call)
    for job_id in ('job-electrician', 'missing'):
        response = client.post(f'/api/v1/jobs/{job_id}/recommendations', json={})
        assert response.status_code == 403
        assert response.json()['code'] == 'FORBIDDEN'


@pytest.mark.parametrize('role_client', ['VIEWER'], indirect=True)
def test_forbidden_role_precedes_request_field_validation(role_client):
    _, client = role_client
    response = client.post('/api/v1/jobs/job-electrician/recommendations', json={'topK': 0})
    assert response.status_code == 403
    assert response.json()['field_errors'] == []


def test_login_and_health_remain_public(monkeypatch, local_test_account):
    password, secret, user_id, encoded = local_test_account
    monkeypatch.setenv('SKILLMATCH_JWT_SECRET', secret)
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps({'public-login': {
        'user_id': user_id, 'role': 'VIEWER', 'password_hash': encoded}}))
    client = TestClient(app)
    assert client.post('/api/v1/auth/login', json={'username': 'public-login', 'password': password}).status_code == 200
    assert client.get('/health').status_code == 200
    assert client.get('/api/v1/health').status_code == 200


@pytest.mark.parametrize('role_client', ['VIEWER'], indirect=True)
def test_client_supplied_role_cannot_override_signed_role(role_client):
    _, client = role_client
    response = client.post('/api/v1/jobs/job-electrician/recommendations',
                           headers={'X-Role': 'ADMIN'}, json={'role': 'ADMIN'})
    assert response.status_code == 403
    assert response.json()['code'] == 'FORBIDDEN'


def test_every_workforce_route_has_one_enforced_role_policy():
    from fastapi.routing import APIRoute
    for route in app.routes:
        if not isinstance(route, APIRoute) or not route.path.startswith('/api/v1/'):
            continue
        if route.path in ('/api/v1/auth/login', '/api/v1/health'):
            assert not any(getattr(dependency.call, 'allowed_roles', None)
                           for dependency in route.dependant.dependencies)
            continue
        declared = route.openapi_extra['x-allowed-roles']
        enforced = [dependency.call.allowed_roles for dependency in route.dependant.dependencies
                    if hasattr(dependency.call, 'allowed_roles')]
        assert enforced == [tuple(declared)], route.path


def test_invalid_role_policies_fail_closed():
    from skillmatch.features.auth.dependencies import require_roles
    for roles in ((), ('SUPERUSER',)):
        with pytest.raises(ValueError):
            require_roles(*roles)
