from concurrent.futures import ThreadPoolExecutor
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from skillmatch.main import app


@pytest.mark.parametrize('method,path,payload,status,code', [
    ('get', '/api/v1/employees/missing', None, 404, 'NOT_FOUND'),
    ('get', '/unknown', None, 404, 'NOT_FOUND'),
    ('post', '/health', None, 405, 'METHOD_NOT_ALLOWED'),
    ('post', '/api/v1/jobs/job-electrician/recommendations', {'topK': 0}, 422, 'VALIDATION_ERROR'),
])
def test_problem_responses(method, path, payload, status, code, client):
    response = client.request(method, path, json=payload)
    body = response.json()
    assert response.status_code == status
    assert response.headers['content-type'] == 'application/problem+json'
    assert body['type'] == 'about:blank'
    assert body['status'] == status
    assert body['code'] == code
    assert body['detail']
    assert body['request_id'] == response.headers['x-request-id']
    UUID(body['request_id'])
    assert isinstance(body['field_errors'], list)
    if status == 422:
        assert body['field_errors'][0]['field'] == 'body.topK'
        assert body['field_errors'][0]['message']
    if status == 405:
        assert response.headers['allow'] == 'GET'


def test_success_and_documentation_have_request_ids(client):
    for path in ['/health', '/api/v1/employees', '/docs', '/openapi.json']:
        response = client.get(path)
        UUID(response.headers['x-request-id'])
    assert client.get('/health', headers={'X-Request-ID': 'trace-123'}).headers['x-request-id'] == 'trace-123'
    response = client.get('/unknown', headers={'X-Request-ID': 'trace-123'})
    assert response.json()['request_id'] == 'trace-123'


def test_invalid_request_id_is_replaced(client):
    UUID(client.get('/health', headers={'X-Request-ID': 'bad id'}).headers['x-request-id'])


def test_unexpected_error_is_generic_and_correlated(monkeypatch, client):
    def fail():
        raise RuntimeError('private database password')
    monkeypatch.setattr('skillmatch.features.employees.router.get_employees', fail)
    response = TestClient(app, raise_server_exceptions=False).get('/api/v1/employees', headers={'X-Request-ID': 'failure-123', 'Authorization': client.headers['Authorization']})
    assert response.status_code == 500
    assert response.headers['content-type'] == 'application/problem+json'
    assert response.headers['x-request-id'] == response.json()['request_id'] == 'failure-123'
    assert response.json()['code'] == 'INTERNAL_ERROR'
    assert 'password' not in response.text


def test_request_ids_are_isolated_between_concurrent_requests(client):
    def fetch(index):
        request_id = f'trace-{index}'
        response = client.get('/unknown', headers={'X-Request-ID': request_id})
        assert response.headers['x-request-id'] == response.json()['request_id'] == request_id
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fetch, range(12)))


def test_recommendation_metadata(client):
    first = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    second = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    UUID(first.json()['match_run_id'])
    assert first.json()['match_run_id'] != second.json()['match_run_id']
    assert first.json()['model_version'] == second.json()['model_version'] == 'rpce-55-20-15-10-v1'
    UUID(first.headers['x-request-id'])


def test_malformed_json_has_serializable_field_errors(client):
    response = client.post('/api/v1/jobs/job-electrician/recommendations', content='{', headers={'Content-Type': 'application/json'})
    assert response.status_code == 422
    assert response.json()['field_errors'][0]['code'] == 'json_invalid'
    assert response.json()['request_id'] == response.headers['x-request-id']


def test_openapi_documents_problem_shape_and_response_headers(client):
    schema = client.get('/openapi.json').json()
    assert 'FieldError' in schema['components']['schemas']
    assert schema['components']['schemas']['ProblemDetails']['properties']['field_errors']['items']['$ref'] == '#/components/schemas/FieldError'
    for path in schema['paths'].values():
        for operation in path.values():
            for response in operation['responses'].values():
                assert 'X-Request-ID' in response['headers']
            for status in ('404', '422', '500'):
                content = operation['responses'][status]['content']
                assert set(content) == {'application/problem+json'}
                assert content['application/problem+json']['schema']['$ref'] == '#/components/schemas/ProblemDetails'
