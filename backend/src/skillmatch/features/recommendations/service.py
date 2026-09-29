from skillmatch.features.employees.repository import get_employees
from skillmatch.features.jobs.schemas import Job
from skillmatch.features.matching.ranking import rank_recommendations
from skillmatch.features.matching.scoring import build_recommendation
from skillmatch.features.matching.schemas import (
    EmployeeInput,
    JobInput,
    Recommendation,
)


def recommend_employees(
    job: Job,
    candidate_employee_ids: list[str] | None,
    top_k: int,
    minimum_score: float,
    include_missing_skills: bool,
) -> list[Recommendation]:
    job_input = JobInput.model_validate(job.model_dump())
    recommendations = [
        build_recommendation(
            EmployeeInput.model_validate(employee.model_dump()), job_input
        )
        for employee in get_employees(candidate_employee_ids)
    ]
    if not include_missing_skills:
        recommendations = [
            recommendation.model_copy(update={"missing_requirements": []})
            for recommendation in recommendations
        ]
    return rank_recommendations(recommendations, minimum_score, top_k)
