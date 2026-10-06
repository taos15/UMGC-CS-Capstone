"""Validate and load the approved demo dataset; never overwrite existing profiles."""
import json
from pathlib import Path
from sqlmodel import Session
from skillmatch.db.session import engine, init_db
from skillmatch.features.employees.schemas import EmployeeProfile, EmployeeCreate
from skillmatch.features.jobs.schemas import JobProfile, JobCreate
from skillmatch.features.employees.models import EmployeeRecord
from skillmatch.features.jobs.models import JobRecord
from skillmatch.features.skills.models import SkillRecord

DATA = Path(__file__).resolve().parents[1] / 'data/mock'


def seed_data():
    skills = json.loads((DATA / 'skills.json').read_text())
    employees = [EmployeeProfile.model_validate(row) for row in json.loads((DATA / 'employees.json').read_text())]
    jobs = [JobProfile.model_validate(row) for row in json.loads((DATA / 'jobs.json').read_text())]
    for profile in employees:
        EmployeeCreate.model_validate(profile.model_dump(exclude={'id', 'version'}))
        if any(item.skill_id not in skills for item in profile.skills):
            raise ValueError('Unknown employee skill')
    for profile in jobs:
        JobCreate.model_validate(profile.model_dump(exclude={'id', 'version'}))
        if any(item.skill_id not in skills for item in profile.skill_requirements):
            raise ValueError('Unknown job skill')
    init_db()
    with Session(engine) as session:
        try:
            for skill in skills:
                if session.get(SkillRecord, skill) is None:
                    session.add(SkillRecord(skill_id=skill))
            for profile in employees:
                if session.get(EmployeeRecord, profile.id) is None:
                    session.add(EmployeeRecord(id=profile.id, employee_number=profile.employee_number,
                        version=profile.version, payload=profile.model_dump(mode='json')))
            for profile in jobs:
                if session.get(JobRecord, profile.id) is None:
                    session.add(JobRecord(id=profile.id, job_code=profile.job_code,
                        version=profile.version, payload=profile.model_dump(mode='json')))
            session.commit()
        except Exception:
            session.rollback()
            raise
    print('Validated demo dataset loaded; existing profiles retained.')


if __name__ == '__main__':
    seed_data()
