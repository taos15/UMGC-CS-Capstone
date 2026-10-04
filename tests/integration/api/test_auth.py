import json
import secrets
from datetime import datetime, timezone
from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient

from skillmatch.main import app


@pytest.fixture
def configured_auth(monkeypatch):
    from skillmatch.core.security import hash_password
    password = secrets.token_urlsafe(24)
    secret = secrets.token_urlsafe(48)
    user_id = str(uuid4())
    monkeypatch.setenv('SKILLMATCH_JWT_SECRET', secret)
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps({
        'supervisor': {'user_id': user_id, 'role': 'SUPERVISOR', 'password_hash': hash_password(password)}
    }))
    return TestClient(app), password, secret, user_id


def test_login_issues_short_lived_signed_token(configured_auth):
    client, password, secret, user_id = configured_auth
    before = int(datetime.now(timezone.utc).timestamp())
    response = client.post('/api/v1/auth/login', json={'username': 'supervisor', 'password': password})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {'access_token', 'token_type', 'expires_in'}
    assert body['token_type'] == 'bearer'
    assert body['expires_in'] == 900
    claims = jwt.decode(body['access_token'], secret, algorithms=['HS256'])
    assert claims['sub'] == user_id
    assert claims['role'] == 'SUPERVISOR'
    assert before <= claims['iat'] <= int(datetime.now(timezone.utc).timestamp())
    assert claims['exp'] - claims['iat'] == 900
    assert response.headers['cache-control'] == 'no-store'
    assert response.headers['x-request-id']
    assert client.get('/api/v1/employees', headers={'Authorization': 'Bearer ' + body['access_token']}).status_code == 200


def test_login_failures_do_not_enumerate_users(configured_auth):
    client, password, _, _ = configured_auth
    responses = [client.post('/api/v1/auth/login', json=credentials, headers={'X-Request-ID': 'same-trace'})
                 for credentials in ({'username': 'supervisor', 'password': 'wrong'},
                                     {'username': 'unknown', 'password': password})]
    assert responses[0].json() == responses[1].json()
    for response in responses:
        assert response.status_code == 401
        assert response.headers['content-type'] == 'application/problem+json'
        assert response.headers['www-authenticate'] == 'Bearer'
        assert response.json()['code'] == 'AUTH_INVALID_CREDENTIALS'
        assert response.json()['detail'] == 'Invalid username or password.'
        assert response.json()['request_id'] == response.headers['x-request-id']


@pytest.mark.parametrize('kind', ['missing', 'malformed', 'expired', 'tampered', 'wrong_algorithm', 'missing_claim'])
def test_protected_routes_reject_invalid_tokens(configured_auth, kind):
    client, _, secret, user_id = configured_auth
    now = int(datetime.now(timezone.utc).timestamp())
    claims = {'sub': user_id, 'role': 'SUPERVISOR', 'iat': now, 'exp': now + 900}
    headers = {}
    if kind == 'expired':
        claims.update(iat=now-1000, exp=now-100)
    if kind == 'missing_claim':
        claims.pop('role')
    if kind != 'missing':
        token = jwt.encode(claims, secrets.token_urlsafe(48) if kind == 'tampered' else secret,
                           algorithm='HS384' if kind == 'wrong_algorithm' else 'HS256')
        headers['Authorization'] = 'Bearer ' + ('garbage' if kind == 'malformed' else token)
    response = client.get('/api/v1/employees', headers=headers)
    assert response.status_code == 401
    assert response.json()['code'] == 'AUTH_REQUIRED'
    assert response.headers['www-authenticate'] == 'Bearer'


def test_unconfigured_auth_fails_closed(monkeypatch):
    monkeypatch.delenv('SKILLMATCH_JWT_SECRET', raising=False)
    monkeypatch.delenv('SKILLMATCH_LOCAL_USERS', raising=False)
    response = TestClient(app).post('/api/v1/auth/login', json={'username': 'any', 'password': 'any'})
    assert response.status_code == 503
    assert response.json()['code'] == 'AUTH_UNAVAILABLE'


def test_password_not_exposed_in_validation_errors(configured_auth):
    client, password, _, _ = configured_auth
    response = client.post('/api/v1/auth/login', json={'password': password})
    assert response.status_code == 422
    assert password not in response.text
    assert response.headers['content-type'] == 'application/problem+json'


@pytest.mark.parametrize('method,path', [
    ('get', '/api/v1/skills'), ('post', '/api/v1/skills'),
    ('get', '/api/v1/employees'), ('post', '/api/v1/employees'),
    ('get', '/api/v1/employees/unknown'), ('put', '/api/v1/employees/unknown'),
    ('get', '/api/v1/jobs'), ('post', '/api/v1/jobs'),
    ('get', '/api/v1/jobs/unknown'), ('put', '/api/v1/jobs/unknown'),
    ('post', '/api/v1/jobs/unknown/recommendations'),
    ('get', '/api/v1/match-runs/unknown'), ('post', '/api/v1/match-runs/unknown/feedback'),
])
def test_all_workforce_routes_require_authentication(method, path):
    response = TestClient(app).request(method, path)
    assert response.status_code == 401
    assert response.json()['code'] == 'AUTH_REQUIRED'


def test_unknown_user_performs_password_verification(configured_auth, monkeypatch):
    from skillmatch.features.auth import service
    original = service.verify_password
    calls = []
    def verify(password, encoded):
        calls.append(encoded)
        return original(password, encoded)
    monkeypatch.setattr(service, 'verify_password', verify)
    client, _, _, _ = configured_auth
    for username in ('supervisor', 'unknown'):
        assert client.post('/api/v1/auth/login', json={'username': username, 'password': 'wrong'}).status_code == 401
    assert len(calls) == 2
    assert all(encoded.startswith('scrypt$') for encoded in calls)


@pytest.mark.parametrize('setting,value', [
    ('SKILLMATCH_JWT_SECRET', 'short'),
    ('SKILLMATCH_LOCAL_USERS', '{invalid json'),
    ('SKILLMATCH_LOCAL_USERS', '{}'),
    ('SKILLMATCH_LOCAL_USERS', '{"user":{"user_id":"bad","role":"ADMIN","password_hash":"invalid"}}'),
])
def test_bad_configuration_is_generic(configured_auth, monkeypatch, setting, value):
    client, password, _, _ = configured_auth
    monkeypatch.setenv(setting, value)
    response = client.post('/api/v1/auth/login', json={'username': 'supervisor', 'password': password})
    assert response.status_code == 503
    assert response.json()['code'] == 'AUTH_UNAVAILABLE'
    assert password not in response.text
    assert value not in response.text


def test_openapi_documents_authentication_contract():
    schema = app.openapi()
    login = schema['paths']['/api/v1/auth/login']['post']
    assert login['security'] == []
    assert '200' in login['responses']
    assert '501' not in login['responses']
    for status in ('401', '422', '503'):
        assert set(login['responses'][status]['content']) == {'application/problem+json'}
    assert schema['paths']['/api/v1/employees']['get']['security'] == [{'HTTPBearer': []}]
