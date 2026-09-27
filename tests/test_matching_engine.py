from app.data import EMPLOYEES, JOBS
from app.matching_engine import build_recommendation


def test_exact_candidate_receives_full_score() -> None:
    recommendation = build_recommendation(EMPLOYEES[0], JOBS[0])

    assert recommendation.score == 100
    assert recommendation.missing_requirements == []
    assert recommendation.matched_skills == JOBS[0].required_skills
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
