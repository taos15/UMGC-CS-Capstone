from datetime import date

import pytest
from pydantic import ValidationError

from skillmatch.features.matching.canonical_scoring import (
    EmployeeScoringInput, JobScoringInput, SkillProficiency, SkillRequirement, score_candidate,
)
from skillmatch.features.matching.eligibility import (
    CertificationEvidence, EmployeeEligibilityInput, evaluate_eligibility,
)

SNAPSHOT = date(2026, 10, 4)


def credential(code='license', issued_on=date(2020, 1, 1), expires_on=None):
    return CertificationEvidence(code=code, issued_on=issued_on, expires_on=expires_on)


def job(codes=frozenset({'license'})):
    return JobScoringInput(
        skill_requirements=(SkillRequirement(skill_id='required', level='REQUIRED', minimum_proficiency=4, importance=1),),
        required_certification_codes=codes, minimum_years_experience=0,
    )


@pytest.mark.parametrize('status', ['INACTIVE', 'ON_LEAVE', 'TERMINATED', 'active', 'UNKNOWN'])
def test_only_active_employees_are_eligible(status):
    employee = EmployeeEligibilityInput(status=status, certifications=(credential(),))
    result = evaluate_eligibility(employee, job(), as_of=SNAPSHOT)
    assert result.eligible is False
    assert result.ineligible_reasons == ('EMPLOYEE_NOT_ACTIVE',)
    assert result.missing_certifications == ()


@pytest.mark.parametrize('certifications,eligible', [
    ((), False),
    ((credential(expires_on=date(2026, 10, 3)),), False),
    ((credential(expires_on=SNAPSHOT),), True),
    ((credential(expires_on=date(2026, 10, 5)),), True),
    ((credential(),), True),
    ((credential(issued_on=date(2026, 10, 5)),), False),
    ((credential(code='unrelated'),), False),
])
def test_mandatory_certification_requires_current_valid_evidence(certifications, eligible):
    employee = EmployeeEligibilityInput(status='ACTIVE', certifications=certifications)
    result = evaluate_eligibility(employee, job(), as_of=SNAPSHOT)
    assert result.eligible is eligible
    assert result.missing_certifications == (() if eligible else ('license',))
    assert result.ineligible_reasons == (() if eligible else ('MISSING_MANDATORY_CERTIFICATION:license',))


def test_reasons_and_evidence_are_stable_for_multiple_failures():
    employee = EmployeeEligibilityInput(status='INACTIVE', certifications=(credential('unrelated'),))
    first = evaluate_eligibility(employee, job(frozenset({'z', 'a'})), as_of=SNAPSHOT)
    second = evaluate_eligibility(employee, job(frozenset({'a', 'z'})), as_of=SNAPSHOT)
    assert first == second
    assert first.ineligible_reasons == ('EMPLOYEE_NOT_ACTIVE', 'MISSING_MANDATORY_CERTIFICATION:a', 'MISSING_MANDATORY_CERTIFICATION:z')
    assert first.missing_certifications == ('a', 'z')
    assert first.matched_certifications == ()


def test_renewed_credential_satisfies_requirement_even_with_expired_duplicate():
    certifications = (credential(expires_on=date(2025, 1, 1)), credential())
    employee = EmployeeEligibilityInput(status='ACTIVE', certifications=certifications)
    result = evaluate_eligibility(employee, job(), as_of=SNAPSHOT)
    reversed_employee = employee.model_copy(update={'certifications': certifications[::-1]})
    assert result == evaluate_eligibility(reversed_employee, job(), as_of=SNAPSHOT)
    assert result.eligible
    assert result.matched_certifications == ('license',)
    assert result.valid_certification_codes == frozenset({'license'})


def test_no_mandatory_credentials_does_not_exclude_active_employee():
    result = evaluate_eligibility(EmployeeEligibilityInput(status='ACTIVE', certifications=()), job(frozenset()), as_of=SNAPSHOT)
    assert result.eligible
    assert result.ineligible_reasons == ()


def test_missing_required_skill_reduces_score_without_exclusion():
    employee = EmployeeEligibilityInput(status='ACTIVE', certifications=(credential(),))
    requirements = job()
    eligibility = evaluate_eligibility(employee, requirements, as_of=SNAPSHOT)
    missing_skill = EmployeeScoringInput(skills=(), valid_certification_codes=eligibility.valid_certification_codes, total_years_experience=0)
    has_skill = missing_skill.model_copy(update={'skills': (SkillProficiency(skill_id='required', proficiency=4),)})
    assert eligibility.eligible
    assert score_candidate(missing_skill, requirements).score < score_candidate(has_skill, requirements).score
    assert score_candidate(missing_skill, requirements).required_skills == 0


def test_fixed_snapshot_controls_validity_and_inputs_are_immutable():
    employee = EmployeeEligibilityInput(status='ACTIVE', certifications=(credential(expires_on=SNAPSHOT),))
    original = employee.model_dump()
    result = evaluate_eligibility(employee, job(), as_of=SNAPSHOT)
    assert result == evaluate_eligibility(employee, job(), as_of=SNAPSHOT)
    assert not evaluate_eligibility(employee, job(), as_of=date(2026, 10, 5)).eligible
    assert employee.model_dump() == original
    with pytest.raises(ValidationError):
        employee.status = 'INACTIVE'
    with pytest.raises(ValidationError):
        employee.certifications[0].code = 'changed'


def test_certification_issued_on_snapshot_is_valid():
    result = evaluate_eligibility(
        EmployeeEligibilityInput(status='ACTIVE', certifications=(credential(issued_on=SNAPSHOT),)),
        job(), as_of=SNAPSHOT,
    )
    assert result.eligible
    assert result.matched_certifications == ('license',)


def test_future_renewal_does_not_rescue_expired_credential():
    employee = EmployeeEligibilityInput(status='ACTIVE', certifications=(
        credential(expires_on=date(2026, 10, 3)),
        credential(issued_on=date(2026, 10, 5)),
    ))
    result = evaluate_eligibility(employee, job(), as_of=SNAPSHOT)
    assert not result.eligible
    assert result.valid_certification_codes == frozenset()
    assert result.missing_certifications == ('license',)
    assert result.ineligible_reasons == ('MISSING_MANDATORY_CERTIFICATION:license',)


def test_every_mandatory_certification_must_be_valid():
    employee = EmployeeEligibilityInput(status='ACTIVE', certifications=(
        credential('a'), credential('z', expires_on=date(2026, 10, 3)), credential('unrelated'),
    ))
    result = evaluate_eligibility(employee, job(frozenset({'a', 'z'})), as_of=SNAPSHOT)
    assert not result.eligible
    assert result.matched_certifications == ('a',)
    assert result.missing_certifications == ('z',)
    assert result.ineligible_reasons == ('MISSING_MANDATORY_CERTIFICATION:z',)
