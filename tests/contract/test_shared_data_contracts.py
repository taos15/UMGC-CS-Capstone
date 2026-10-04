from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from skillmatch.features.employees.schemas import EmployeeCertification, EmployeeProfile, EmployeeSkill
from skillmatch.features.feedback.schemas import Feedback
from skillmatch.features.jobs.schemas import JobProfile, JobSkillRequirement
from skillmatch.features.matching.schemas import CandidateResult
from skillmatch.features.recommendations.schemas import MatchRun, RecommendationOptions


@pytest.mark.parametrize('model,fields', [
    (EmployeeSkill, 'skill_id proficiency years_experience last_used_on'),
    (EmployeeCertification, 'code name issuer issued_on expires_on'),
    (EmployeeProfile, 'id employee_number name current_title status total_years_experience version skills certifications'),
    (JobSkillRequirement, 'skill_id level minimum_proficiency importance'),
    (JobProfile, 'id job_code title description status minimum_years_experience version skill_requirements certification_requirements'),
    (RecommendationOptions, 'max_results minimum_score include_ineligible'),
    (CandidateResult, 'rank employee_id score eligible component_scores matched_skills missing_skills matched_certifications missing_certifications ineligible_reasons explanation'),
    (MatchRun, 'match_run_id job_id requested_by model_version snapshot_hash options generated_at results'),
    (Feedback, 'match_run_id user_id decision selected_employee_id rating comment created_at'),
])
def test_contract_fields_are_snake_case(model, fields):
    assert set(model.model_fields) == set(fields.split())
    assert all(field.alias is None for field in model.model_fields.values())


@pytest.mark.parametrize('model,payload', [
    (EmployeeSkill, dict(skill_id='python', proficiency=0, years_experience=1)),
    (EmployeeSkill, dict(skill_id='python', proficiency=6, years_experience=1)),
    (EmployeeSkill, dict(skill_id='python', proficiency=3, years_experience=-1)),
    (JobSkillRequirement, dict(skill_id='python', level='OTHER', minimum_proficiency=3, importance=1)),
    (JobSkillRequirement, dict(skill_id='python', level='REQUIRED', minimum_proficiency=6, importance=1)),
    (JobSkillRequirement, dict(skill_id='python', level='PREFERRED', minimum_proficiency=3, importance=4)),
    (RecommendationOptions, dict(max_results=101, minimum_score=0, include_ineligible=False)),
    (RecommendationOptions, dict(max_results=1, minimum_score=-1, include_ineligible=False)),
    (Feedback, dict(match_run_id='run', user_id='user', decision='ASSIGNED', created_at=datetime.now(timezone.utc))),
])
def test_invalid_contract_values_are_rejected(model, payload):
    with pytest.raises(ValidationError):
        model.model_validate(payload)


def test_run_nested_contract_json_round_trip():
    run = MatchRun.model_validate(dict(
        match_run_id='run', job_id='job', requested_by='user', model_version='v1',
        snapshot_hash='hash', options=dict(max_results=1, minimum_score=0, include_ineligible=False),
        generated_at='2026-10-04T12:00:00Z', results=[dict(
            rank=1, employee_id='employee', score=100, eligible=True,
            component_scores={'experience': 1}, matched_skills=['python'], missing_skills=[],
            matched_certifications=[], missing_certifications=[], ineligible_reasons=[], explanation='Qualified',
        )],
    ))
    assert isinstance(run.results[0], CandidateResult)
    assert MatchRun.model_validate_json(run.model_dump_json()) == run
