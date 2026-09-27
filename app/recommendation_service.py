from app.employee_service import get_employees
from app.matching_engine import build_recommendation
from app.schemas import Job, Recommendation


def recommend_employees(
    job: Job,
    candidate_employee_ids: list[str] | None,
    top_k: int,
    minimum_score: float,
    include_missing_skills: bool,
) -> list[Recommendation]:
    recommendations = [
        build_recommendation(employee, job)
        for employee in get_employees(candidate_employee_ids)
    ]
    if not include_missing_skills:
        recommendations = [
            recommendation.model_copy(update={"missing_requirements": []})
            for recommendation in recommendations
        ]
    return sorted(
        (
            recommendation
            for recommendation in recommendations
            if recommendation.score >= minimum_score
        ),
        key=lambda recommendation: recommendation.score,
        reverse=True,
    )[:top_k]
