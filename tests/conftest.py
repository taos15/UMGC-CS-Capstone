"""Authenticated API clients use ephemeral test-only local credentials."""

import json
import secrets
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope='session')
def local_test_account():
    from skillmatch.core.security import hash_password
    password = secrets.token_urlsafe(24)
    return password, secrets.token_urlsafe(48), str(uuid4()), hash_password(password)


@pytest.fixture
def client(monkeypatch, local_test_account):
    from skillmatch.main import app
    password, secret, user_id, encoded = local_test_account
    monkeypatch.setenv('SKILLMATCH_JWT_SECRET', secret)
    monkeypatch.setenv('SKILLMATCH_LOCAL_USERS', json.dumps({
        'test-admin': {'user_id': user_id, 'role': 'ADMIN', 'password_hash': encoded}
    }))
    with TestClient(app) as api_client:
        response = api_client.post('/api/v1/auth/login', json={'username': 'test-admin', 'password': password})
        assert response.status_code == 200
        api_client.headers['Authorization'] = 'Bearer ' + response.json()['access_token']
        yield api_client
