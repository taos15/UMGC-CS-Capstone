import pytest
from fastapi.testclient import TestClient

from skillmatch.main import app

READ = ['ADMIN', 'SUPERVISOR', 'VIEWER']
WRITE = ['ADMIN']
SUPERVISE = ['ADMIN', 'SUPERVISOR']
OPERATIONS = [
    ('post', '/api/v1/auth/login', [], False),
    ('get', '/api/v1/skills', READ, True),
    ('post', '/api/v1/skills', WRITE, True),
    ('get', '/api/v1/employees', READ, False),
    ('post', '/api/v1/employees', WRITE, True),
    ('get', '/api/v1/employees/{employee_id}', READ, False),
    ('put', '/api/v1/employees/{employee_id}', WRITE, True),
    ('get', '/api/v1/jobs', READ, True),
    ('post', '/api/v1/jobs', WRITE, True),
    ('get', '/api/v1/jobs/{job_id}', READ, False),
    ('put', '/api/v1/jobs/{job_id}', WRITE, True),
    ('post', '/api/v1/jobs/{job_id}/recommendations', SUPERVISE, False),
    ('get', '/api/v1/match-runs/{match_run_id}', READ, True),
    ('post', '/api/v1/match-runs/{match_run_id}/feedback', SUPERVISE, True),
    ('get', '/api/v1/health', None, False),
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


@pytest.mark.parametrize('method,path,roles,is_stub', [item for item in OPERATIONS if item[3]])
def test_stubs_explicitly_report_unimplemented(method, path, roles, is_stub, client):
    path = path.replace('{employee_id}', 'employee').replace('{job_id}', 'job').replace('{match_run_id}', 'run')
    response = client.request(method, path)
    assert response.status_code == 501
    assert response.json()['detail'] == 'Not implemented'


def test_versioned_health():
    response = TestClient(app).get('/api/v1/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'database': 'ok'}
