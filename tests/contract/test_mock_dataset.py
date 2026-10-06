"""Mock fixture integrity and observed matching spread, not guessed scores."""
import json
import runpy
from pathlib import Path
from uuid import UUID

from skillmatch.features.employees.schemas import EmployeeProfile
from skillmatch.features.jobs.schemas import JobProfile

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'mock'


def read(name):
    return json.loads((DATA / name).read_text())


def test_mock_dataset_counts_keys_and_references():
    employees = [EmployeeProfile.model_validate(value) for value in read('employees.json')]
    jobs = [JobProfile.model_validate(value) for value in read('jobs.json')]
    skills = read('skills.json')
    codes = read('certification_codes.json')
    assert len(employees) == 10
    assert len(jobs) == 3
    assert 10 <= len(skills) <= 15
    assert len(set(skills)) == len(skills)
    assert len(set(codes)) == len(codes) == 3
    assert len({employee.employee_number for employee in employees}) == 10
    assert len({job.job_code for job in jobs}) == 3
    ids = [record.id for record in employees + jobs]
    assert len(set(ids)) == 13
    for value in ids:
        UUID(value)
    for employee in employees:
        assert employee.version > 0
        assert len({skill.skill_id for skill in employee.skills}) == len(employee.skills)
        assert {skill.skill_id for skill in employee.skills} <= set(skills)
        assert {cert.code for cert in employee.certifications} <= set(codes)
        for skill in employee.skills:
            assert skill.years_experience <= employee.total_years_experience
        for cert in employee.certifications:
            assert cert.expires_on is None or cert.issued_on <= cert.expires_on
    for job in jobs:
        assert job.status == 'OPEN'
        assert {requirement.skill_id for requirement in job.skill_requirements} <= set(skills)
        assert set(job.certification_requirements) <= set(codes)
    assert {skill.skill_id for employee in employees for skill in employee.skills} == set(skills)


def test_every_job_has_high_medium_and_low_eligible_candidates():
    build_preview = runpy.run_path(str(ROOT / 'scripts' / 'preview_mock_dataset.py'))['build_preview']
    preview = build_preview()
    assert preview == read('score_preview.json')
    assert build_preview() == preview
    for job in preview['jobs']:
        scores = [candidate['score'] for candidate in job['candidates'] if candidate['eligible']]
        assert any(score >= 85 for score in scores), job['title']
        assert any(40 <= score <= 80 for score in scores), job['title']
        assert any(score <= 35 for score in scores), job['title']
        inactive = next(candidate for candidate in job['candidates'] if candidate['employee_number'] == 'MOCK-E010')
        assert not inactive['eligible']
        assert 'EMPLOYEE_NOT_ACTIVE' in inactive['ineligible_reasons']
    maintenance = next(job for job in preview['jobs'] if job['job_code'] == 'MOCK-J003')
    expired = next(candidate for candidate in maintenance['candidates'] if candidate['employee_number'] == 'MOCK-E009')
    assert not expired['eligible']
    assert 'MISSING_MANDATORY_CERTIFICATION:osha 10' in expired['ineligible_reasons']
