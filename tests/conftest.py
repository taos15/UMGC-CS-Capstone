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


@pytest.fixture(autouse=True)
def test_database(monkeypatch, request):
    """Each test starts from persisted compatibility fixtures, never the user's DB."""
    if '/integration/api/' not in str(request.fspath) and request.fspath.basename != 'test_endpoint_contract.py':
        yield
        return
    from sqlalchemy.pool import StaticPool
    from sqlmodel import SQLModel, Session, create_engine
    from skillmatch.db import session as database
    from skillmatch import main
    from skillmatch.features.employees.models import EmployeeRecord
    from skillmatch.features.jobs.models import JobRecord
    from skillmatch.features.skills.models import SkillRecord
    from skillmatch.features.employees.schemas import EmployeeProfile
    from skillmatch.features.jobs.schemas import JobProfile
    from skillmatch.features.employees.seed import EMPLOYEES
    from skillmatch.features.jobs.seed import JOBS

    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr(database, 'engine', engine)
    monkeypatch.setattr(main, 'engine', engine)
    with Session(engine) as session:
        codes = {item.skill_id for employee in EMPLOYEES for item in employee.skill_evidence}
        codes.update(item.skill_id for job in JOBS for item in job.skill_requirement_details)
        session.add_all([SkillRecord(skill_id=code) for code in codes])
        for employee in EMPLOYEES:
            profile = EmployeeProfile(id=employee.id, employee_number=employee.id,
                name=employee.name, current_title='Technician', status=employee.status,
                total_years_experience=employee.years_experience, version=1,
                skills=employee.skill_evidence, certifications=employee.certification_evidence)
            session.add(EmployeeRecord(id=profile.id, employee_number=profile.employee_number,
                                       payload=profile.model_dump(mode='json')))
        for job in JOBS:
            profile = JobProfile(id=job.id, job_code=job.id, title=job.title, description=job.title,
                status=job.status, minimum_years_experience=job.minimum_years_experience,
                version=1, skill_requirements=job.skill_requirement_details,
                certification_requirements=job.required_certifications)
            session.add(JobRecord(id=profile.id, job_code=profile.job_code, payload=profile.model_dump(mode='json')))
        session.commit()
    yield
    engine.dispose()
