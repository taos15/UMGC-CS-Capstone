from itertools import product

import pytest
from pydantic import ValidationError

from skillmatch.features.matching.canonical_scoring import (
    EmployeeScoringInput,
    JobScoringInput,
    SkillProficiency,
    SkillRequirement,
    score_candidate,
)


def requirement(skill_id="skill", level="REQUIRED", minimum=4, importance=1):
    return SkillRequirement(
        skill_id=skill_id, level=level,
        minimum_proficiency=minimum, importance=importance,
    )


def test_weighted_proficiency_certifications_and_experience():
    employee = EmployeeScoringInput(
        skills=(
            SkillProficiency(skill_id="required", proficiency=2),
            SkillProficiency(skill_id="preferred-a", proficiency=5),
            SkillProficiency(skill_id="preferred-b", proficiency=1),
        ),
        valid_certification_codes=frozenset({"valid", "unrelated"}),
        total_years_experience=2,
    )
    job = JobScoringInput(
        skill_requirements=(
            requirement("required", importance=3),
            requirement("missing"),
            requirement("preferred-a", "PREFERRED", minimum=2),
            requirement("preferred-b", "PREFERRED", minimum=2),
        ),
        required_certification_codes=frozenset({"valid", "expired"}),
        minimum_years_experience=4,
    )

    result = score_candidate(employee, job)

    assert result.required_skills == pytest.approx(0.375)
    assert result.preferred_skills == pytest.approx(0.75)
    assert result.required_certifications == pytest.approx(0.5)
    assert result.experience == pytest.approx(0.5)
    assert result.score == pytest.approx(48.125)
    assert result.model_version == "rpce-55-20-15-10-v1"
    assert score_candidate(employee, job) == result


@pytest.mark.parametrize("level", ["REQUIRED", "PREFERRED"])
def test_both_skill_categories_use_importance_and_cap_each_skill(level):
    employee = EmployeeScoringInput(
        skills=(SkillProficiency(skill_id="present", proficiency=5),),
        valid_certification_codes=frozenset(), total_years_experience=0,
    )
    job = JobScoringInput(
        skill_requirements=(
            requirement("present", level, minimum=2, importance=1),
            requirement("missing", level, importance=3),
        ),
        required_certification_codes=frozenset(), minimum_years_experience=0,
    )
    result = score_candidate(employee, job)
    component = result.required_skills if level == "REQUIRED" else result.preferred_skills
    assert component == 0.25


@pytest.mark.parametrize("has_r,has_p,has_c", list(product([False, True], repeat=3)))
def test_absent_categories_are_removed_and_weights_renormalized(has_r, has_p, has_c):
    requirements = []
    if has_r:
        requirements.append(requirement("r"))
    if has_p:
        requirements.append(requirement("p", "PREFERRED"))
    employee = EmployeeScoringInput(
        skills=(), valid_certification_codes=frozenset(), total_years_experience=1,
    )
    job = JobScoringInput(
        skill_requirements=tuple(requirements),
        required_certification_codes=frozenset({"cert"}) if has_c else frozenset(),
        minimum_years_experience=2,
    )
    result = score_candidate(employee, job)
    assert result.required_skills == (0.0 if has_r else None)
    assert result.preferred_skills == (0.0 if has_p else None)
    assert result.required_certifications == (0.0 if has_c else None)
    assert result.score == pytest.approx(100 * 10 * 0.5 / (55 * has_r + 20 * has_p + 15 * has_c + 10))


@pytest.mark.parametrize("years,minimum,expected", [(0, 0, 1), (0, 2, 0), (1, 2, 0.5), (2, 2, 1), (9, 2, 1)])
def test_experience_zero_minimum_partial_and_capped(years, minimum, expected):
    employee = EmployeeScoringInput(
        skills=(), valid_certification_codes=frozenset(), total_years_experience=years,
    )
    job = JobScoringInput(
        skill_requirements=(requirement(),),
        required_certification_codes=frozenset(), minimum_years_experience=minimum,
    )
    assert score_candidate(employee, job).experience == expected


@pytest.mark.parametrize("proficiency,years,certs,expected", [(1, 0, (), 0), (5, 20, ("cert",), 100)])
def test_score_extremes(proficiency, years, certs, expected):
    employee = EmployeeScoringInput(
        skills=() if expected == 0 else (SkillProficiency(skill_id="skill", proficiency=proficiency),),
        valid_certification_codes=frozenset(certs), total_years_experience=years,
    )
    job = JobScoringInput(
        skill_requirements=(requirement(),),
        required_certification_codes=frozenset({"cert"}), minimum_years_experience=2,
    )
    assert score_candidate(employee, job).score == expected


def test_inputs_and_results_are_deeply_immutable():
    skills = [SkillProficiency(skill_id="skill", proficiency=2)]
    employee = EmployeeScoringInput(
        skills=skills, valid_certification_codes={"cert"}, total_years_experience=1,
    )
    job = JobScoringInput(
        skill_requirements=[requirement()],
        required_certification_codes={"cert"}, minimum_years_experience=2,
    )
    skills.clear()
    assert len(employee.skills) == 1
    assert isinstance(employee.skills, tuple)
    assert isinstance(job.skill_requirements, tuple)
    assert isinstance(employee.valid_certification_codes, frozenset)
    assert isinstance(job.required_certification_codes, frozenset)
    result = score_candidate(employee, job)
    for target, field, value in (
        (employee, "total_years_experience", 5),
        (employee.skills[0], "proficiency", 5),
        (job, "minimum_years_experience", 5),
        (job.skill_requirements[0], "importance", 3),
        (result, "score", 100),
    ):
        with pytest.raises(ValidationError, match="frozen"):
            setattr(target, field, value)


@pytest.mark.parametrize("field,value", [
    ("minimum_proficiency", 0), ("minimum_proficiency", 6),
    ("importance", 0), ("importance", 4), ("level", "OTHER"),
])
def test_invalid_skill_requirements_rejected(field, value):
    values = requirement().model_dump()
    values[field] = value
    with pytest.raises(ValidationError):
        SkillRequirement(**values)


@pytest.mark.parametrize("proficiency", [0, 6, 1.5])
def test_invalid_employee_proficiency_rejected(proficiency):
    with pytest.raises(ValidationError):
        SkillProficiency(skill_id="skill", proficiency=proficiency)


@pytest.mark.parametrize("years", [-1, float("nan"), float("inf")])
def test_invalid_experience_rejected(years):
    with pytest.raises(ValidationError):
        EmployeeScoringInput(skills=(), valid_certification_codes=(), total_years_experience=years)
    with pytest.raises(ValidationError):
        JobScoringInput(skill_requirements=(requirement(),), required_certification_codes=(), minimum_years_experience=years)


def test_duplicate_skill_ids_rejected():
    skill = SkillProficiency(skill_id="skill", proficiency=2)
    with pytest.raises(ValidationError, match="Duplicate skill_id"):
        EmployeeScoringInput(skills=(skill, skill), valid_certification_codes=(), total_years_experience=1)
    with pytest.raises(ValidationError, match="Duplicate skill_id"):
        JobScoringInput(skill_requirements=(requirement(), requirement()), required_certification_codes=(), minimum_years_experience=1)


def test_job_without_usable_criteria_rejected():
    with pytest.raises(ValidationError, match="usable scoring criterion"):
        JobScoringInput(skill_requirements=(), required_certification_codes=(), minimum_years_experience=0)


@pytest.mark.parametrize('component,expected_score', [
    ('required_skills', 55), ('preferred_skills', 20),
    ('required_certifications', 15), ('experience', 10),
])
def test_each_component_contributes_its_contract_weight_independently(component, expected_score):
    job = JobScoringInput(
        skill_requirements=(requirement('r'), requirement('p', 'PREFERRED')),
        required_certification_codes={'cert'}, minimum_years_experience=2,
    )
    skill_id = {'required_skills': 'r', 'preferred_skills': 'p'}.get(component)
    employee = EmployeeScoringInput(
        skills=(SkillProficiency(skill_id=skill_id, proficiency=4),) if skill_id else (),
        valid_certification_codes={'cert'} if component == 'required_certifications' else {'unrelated'},
        total_years_experience=2 if component == 'experience' else 0,
    )
    result = score_candidate(employee, job)
    assert result.score == pytest.approx(expected_score)
    for name in ('required_skills', 'preferred_skills', 'required_certifications', 'experience'):
        assert getattr(result, name) == (1 if name == component else 0)
