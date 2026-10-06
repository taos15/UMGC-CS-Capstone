import pytest
from fastapi.testclient import TestClient

from skillmatch.main import app

READ = ['ADMIN', 'SUPERVISOR', 'VIEWER']
WRITE = ['ADMIN']
SUPERVISE = ['ADMIN', 'SUPERVISOR']
OPERATIONS = [
    ('post', '/api/v1/auth/login', [], False),
    ('get', '/api/v1/skills', READ, False),
    ('post', '/api/v1/skills', WRITE, False),
    ('get', '/api/v1/employees', READ, False),
    ('post', '/api/v1/employees', WRITE, False),
    ('get', '/api/v1/employees/{employee_id}', READ, False),
    ('put', '/api/v1/employees/{employee_id}', WRITE, False),
    ('get', '/api/v1/jobs', READ, False),
    ('post', '/api/v1/jobs', WRITE, False),
    ('get', '/api/v1/jobs/{job_id}', READ, False),
    ('put', '/api/v1/jobs/{job_id}', WRITE, False),
    ('post', '/api/v1/jobs/{job_id}/recommendations', SUPERVISE, False),
    ('get', '/api/v1/match-runs/{match_run_id}', READ, False),
    ('post', '/api/v1/match-runs/{match_run_id}/feedback', SUPERVISE, False),
    ('get', '/api/v1/health', None, False),
    ('delete', '/api/v1/employees/{employee_id}', WRITE, False),
    ('delete', '/api/v1/jobs/{job_id}', WRITE, False),
]


@pytest.mark.parametrize('method,path,roles,is_stub', OPERATIONS)
def test_endpoint_role_annotations(method, path, roles, is_stub):
    operation = app.openapi()['paths'][path][method]
    if roles is None:
        assert operation['x-role-policy'] == 'unspecified'
    else:
        assert operation['x-allowed-roles'] == roles
    if path.endswith('/login'):
        assert operation['security'] == []
    if is_stub:
        assert '501' in operation['responses']


@pytest.mark.parametrize('method,path,roles,is_stub', OPERATIONS)
def test_alpha_operations_are_implemented(method, path, roles, is_stub):
    assert not is_stub
    assert '501' not in app.openapi()['paths'][path][method]['responses']


def test_versioned_health():
    response = TestClient(app).get('/api/v1/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'database': 'ok'}
