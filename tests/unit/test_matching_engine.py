import pytest
from pydantic import ValidationError

from skillmatch.features.employees.seed import EMPLOYEES as SEED_EMPLOYEES
from skillmatch.features.jobs.seed import JOBS as SEED_JOBS
from skillmatch.features.matching.ranking import rank_recommendations
from skillmatch.features.matching.schemas import EmployeeInput, JobInput
from skillmatch.features.matching.scoring import build_recommendation


EMPLOYEES = [EmployeeInput.model_validate(item.model_dump()) for item in SEED_EMPLOYEES]
JOBS = [JobInput.model_validate(item.model_dump()) for item in SEED_JOBS]


def test_exact_candidate_receives_full_score() -> None:
    recommendation = build_recommendation(EMPLOYEES[0], JOBS[0])

    assert recommendation.score == 100
    assert recommendation.missing_requirements == []
    assert recommendation.matched_skills == list(JOBS[0].required_skills)
    assert recommendation.score_breakdown.required_skills == 50
    assert recommendation.score_breakdown.preferred_skills == 10
    assert recommendation.score_breakdown.required_certifications == 25
    assert recommendation.score_breakdown.experience == 15
    assert sum(recommendation.score_breakdown.model_dump().values()) == recommendation.score


def test_partial_candidate_reports_missing_requirements() -> None:
    recommendation = build_recommendation(EMPLOYEES[1], JOBS[0])

    assert recommendation.score == 55.33
    assert recommendation.score_breakdown.required_skills == 33.33
    assert recommendation.score_breakdown.preferred_skills == 10
    assert recommendation.score_breakdown.required_certifications == 0
    assert recommendation.score_breakdown.experience == 12
    assert sum(recommendation.score_breakdown.model_dump().values()) == recommendation.score
    assert recommendation.missing_requirements == [
        "blueprint reading",
        "licensed electrician",
    ]


def test_ranking_uses_employee_id_for_equal_scores() -> None:
    first = build_recommendation(EMPLOYEES[0], JOBS[0])
    second = first.model_copy(update={"employee_id": "equal-score"})
    assert rank_recommendations([second, first], 100, 2) == [first, second]
    assert rank_recommendations([first, second], 100, 2) == [first, second]


def test_matching_inputs_are_deeply_immutable() -> None:
    employee = EMPLOYEES[0]
    assert isinstance(employee.skills, tuple)
    assert isinstance(employee.certifications, tuple)
    assert isinstance(JOBS[0].required_skills, tuple)
    with pytest.raises(ValidationError, match="frozen"):
        employee.name = "Changed"


def test_empty_requirements_preserve_full_coverage_score() -> None:
    job = JOBS[0].model_copy(update={
        "required_skills": (), "preferred_skills": (),
        "required_certifications": (), "minimum_years_experience": 0,
    })
    recommendation = build_recommendation(EMPLOYEES[1], job)
    assert recommendation.score == 100
    assert recommendation.missing_requirements == []
