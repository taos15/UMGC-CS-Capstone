from uuid import UUID

import pytest


@pytest.mark.parametrize('kind,fields', [
    ('employees', {'employee_number': 'NEW-1', 'name': 'New employee', 'current_title': 'Technician',
                   'status': 'ACTIVE', 'total_years_experience': 3, 'skills': [], 'certifications': []}),
    ('jobs', {'job_code': 'NEW-1', 'title': 'New job', 'description': 'Test job', 'status': 'OPEN',
              'minimum_years_experience': 1, 'skill_requirements': [], 'certification_requirements': []}),
])
def test_create_update_delete_profiles_with_version_conflicts(client, kind, fields):
    path = f'/api/v1/{kind}'
    created = client.post(path, json=fields)
    assert created.status_code == 201
    record = created.json()
    UUID(record['id'])
    assert record['version'] == 1
    assert client.get(f"{path}/{record['id']}").json() == record
    duplicate = client.post(path, json=fields)
    assert duplicate.status_code == 409
    assert duplicate.json()['code'] == ('EMPLOYEE_EXISTS' if kind == 'employees' else 'JOB_EXISTS')
    updated = client.put(f"{path}/{record['id']}", json={**fields, 'version': 1})
    assert updated.status_code == 200
    assert updated.json()['version'] == 2
    for method in ('put', 'delete'):
        payload = {**fields, 'version': 1} if method == 'put' else {'version': 1}
        stale = client.request(method, f"{path}/{record['id']}", json=payload)
        assert stale.status_code == 409
        assert stale.json()['code'] == 'STALE_VERSION'
    deleted = client.request('DELETE', f"{path}/{record['id']}", json={'version': 2})
    assert deleted.status_code == 204
    assert deleted.content == b''
    assert client.get(f"{path}/{record['id']}").status_code == 404


def test_job_list_is_live_and_paginated(client):
    response = client.get('/api/v1/jobs', params={'page': 1, 'page_size': 1})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert 'skill_requirements' in response.json()[0]


def test_taxonomy_creation_and_unknown_skill_validation(client):
    created = client.post('/api/v1/skills', json={'skill_id': 'new-skill'})
    assert created.status_code == 201
    assert created.json() == 'new-skill'
    assert client.post('/api/v1/skills', json={'skill_id': 'new-skill'}).json()['code'] == 'SKILL_EXISTS'
    assert 'new-skill' in client.get('/api/v1/skills').json()
    fields = {'employee_number': 'SKILL-TEST', 'name': 'Evidence', 'current_title': 'Technician',
        'status': 'ACTIVE', 'total_years_experience': 1, 'certifications': [],
        'skills': [{'skill_id': 'not-in-taxonomy', 'proficiency': 3}]}
    assert client.post('/api/v1/employees', json=fields).status_code == 422
    fields['skills'][0]['skill_id'] = 'new-skill'
    assert client.post('/api/v1/employees', json=fields).status_code == 201


def test_deleting_live_profiles_preserves_stored_recommendations_and_feedback(client):
    result = client.post('/api/v1/jobs/job-electrician/recommendations', json={}).json()
    run_id = result['match_run_id']
    before = client.get(f'/api/v1/match-runs/{run_id}').json()
    assert client.post(f'/api/v1/match-runs/{run_id}/feedback', json={
        'decision': 'SELECTED', 'selected_employee_id': result['recommendations'][0]['employee_id'],
    }).status_code == 201
    for path in ['/api/v1/employees/emp-alex', '/api/v1/jobs/job-electrician']:
        assert client.request('DELETE', path, json={'version': 1}).status_code == 204
    assert client.get(f'/api/v1/match-runs/{run_id}').json() == before


@pytest.mark.parametrize('kind', ['employees', 'jobs'])
def test_invalid_versions_and_unknown_ids(client, kind):
    for version in [0, 1.5, True, '1']:
        response = client.request('DELETE', f'/api/v1/{kind}/missing', json={'version': version})
        assert response.status_code == 422
        assert response.json()['code'] == 'VALIDATION_ERROR'
    response = client.request('DELETE', f'/api/v1/{kind}/missing', json={'version': 1})
    assert response.status_code == 404
    assert response.json()['code'] == ('EMPLOYEE_NOT_FOUND' if kind == 'employees' else 'JOB_NOT_FOUND')


def test_invalid_certification_dates_and_empty_open_job_are_rejected(client):
    fields = {'employee_number': 'DATES', 'name': 'Dates', 'current_title': 'Tech', 'status': 'ACTIVE',
        'total_years_experience': 1, 'skills': [], 'certifications': [
            {'code': 'license', 'issued_on': '2026-10-05', 'expires_on': '2026-10-04'}]}
    assert client.post('/api/v1/employees', json=fields).status_code == 422
    response = client.post('/api/v1/jobs', json={'job_code': 'EMPTY', 'title': 'Empty', 'description': '',
        'status': 'OPEN', 'minimum_years_experience': 0, 'skill_requirements': [], 'certification_requirements': []})
    assert response.status_code == 422
    assert response.json()['code'] == 'JOB_HAS_NO_CRITERIA'


def test_profile_database_errors_are_generic_and_correlated(client, monkeypatch):
    from sqlalchemy.exc import OperationalError
    def unavailable(*args, **kwargs):
        raise OperationalError('private SQL', {}, Exception('private password'))
    monkeypatch.setattr('skillmatch.features.jobs.repository.list_profiles', unavailable)
    # The route's callable is captured explicitly for instrumentation.
    monkeypatch.setattr('skillmatch.features.jobs.router.get_jobs', unavailable)
    response = client.get('/api/v1/jobs')
    assert response.status_code == 503
    assert response.json()['code'] == 'DATABASE_UNAVAILABLE'
    assert response.json()['request_id'] == response.headers['x-request-id']
    assert 'private' not in response.text


def test_evidence_changes_change_snapshot_hash_but_title_is_not_scored(client):
    first = client.post('/api/v1/jobs/job-electrician/recommendations', json={}).json()
    first_run = client.get(f"/api/v1/match-runs/{first['match_run_id']}").json()
    employee = client.get('/api/v1/employees/emp-alex').json()
    fields = {key: value for key, value in employee.items() if key != 'id'}
    fields['current_title'] = 'Unrelated display-only title'
    assert client.put('/api/v1/employees/emp-alex', json=fields).status_code == 200
    same = client.post('/api/v1/jobs/job-electrician/recommendations', json={}).json()
    assert same['recommendations'] == first['recommendations']
    fields['version'] = 2
    fields['total_years_experience'] = 0
    assert client.put('/api/v1/employees/emp-alex', json=fields).status_code == 200
    changed = client.post('/api/v1/jobs/job-electrician/recommendations', json={}).json()
    changed_run = client.get(f"/api/v1/match-runs/{changed['match_run_id']}").json()
    assert changed_run['snapshot_hash'] != first_run['snapshot_hash']
    assert changed['recommendations'][0]['score'] < first['recommendations'][0]['score']
