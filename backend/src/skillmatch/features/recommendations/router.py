from uuid import uuid4

from skillmatch.features.matching.scoring import MODEL_VERSION

from fastapi import APIRouter, HTTPException

from skillmatch.features.jobs.repository import get_job
from skillmatch.features.recommendations.schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from skillmatch.features.recommendations.service import recommend_employees


router = APIRouter()


@router.post(
    "/api/v1/jobs/{job_id}/recommendations",
    response_model=RecommendationResponse,
    openapi_extra={"x-allowed-roles": ["ADMIN", "SUPERVISOR"]},
    description="Allowed roles: ADMIN, SUPERVISOR. Supervisor retains final staffing authority.",
)
def create_recommendations(
    job_id: str, request: RecommendationRequest
) -> RecommendationResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return RecommendationResponse(
        jobId=job.id,
        match_run_id=str(uuid4()),
        model_version=MODEL_VERSION,
        recommendations=recommend_employees(
            job,
            request.candidate_employee_ids,
            request.top_k,
            request.minimum_score,
            request.include_missing_skills,
        ),
    )

READ = {'x-allowed-roles': ['ADMIN', 'SUPERVISOR', 'VIEWER']}
UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.get('/api/v1/match-runs/{match_run_id}', tags=['match-runs'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=READ,
            description='Allowed roles: ADMIN, SUPERVISOR, VIEWER, within authorized run scope.')
def retrieve_match_run(match_run_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
