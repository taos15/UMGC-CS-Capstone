from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from skillmatch.core.errors import ProblemError
from skillmatch.db.session import get_db
from skillmatch.features.auth.dependencies import (
    READ_ROLES,
    SUPERVISOR_ROLES,
    get_authenticated_user,
    role_access,
)
from skillmatch.features.auth.schemas import AuthenticatedUser
from skillmatch.features.jobs.repository import get_job
from skillmatch.features.recommendations.schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from skillmatch.features.recommendations.service import generate_recommendations


router = APIRouter()

PROBLEM_RESPONSES = {
    404: {"description": "Job not found", "content": {"application/problem+json": {
        "schema": {"$ref": "#/components/schemas/ProblemDetails"}}}},
    409: {"description": "Job is not open", "content": {"application/problem+json": {
        "schema": {"$ref": "#/components/schemas/ProblemDetails"}}}},
    422: {"description": "Job has no usable criteria", "content": {"application/problem+json": {
        "schema": {"$ref": "#/components/schemas/ProblemDetails"}}}},
    503: {"description": "Matching or persistence unavailable", "content": {"application/problem+json": {
        "schema": {"$ref": "#/components/schemas/ProblemDetails"}}}},
}


@router.post(
    "/api/v1/jobs/{job_id}/recommendations",
    response_model=RecommendationResponse,
    responses=PROBLEM_RESPONSES,
    **role_access(*SUPERVISOR_ROLES),
    description="Allowed roles: ADMIN, SUPERVISOR. Supervisor retains final staffing authority.",
)
def create_recommendations(
    job_id: str,
    request: RecommendationRequest,
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
) -> RecommendationResponse:
    job = get_job(job_id)
    if job is None:
        raise ProblemError(404, "JOB_NOT_FOUND", "Job not found.")

    match_run_id, model_version, recommendations = generate_recommendations(
        session,
        job,
        requested_by=str(user.user_id),
        candidate_employee_ids=request.candidate_employee_ids,
        top_k=request.top_k,
        minimum_score=request.minimum_score,
        include_missing_skills=request.include_missing_skills,
        include_ineligible=request.include_ineligible,
    )
    return RecommendationResponse(
        jobId=job.id,
        match_run_id=match_run_id,
        model_version=model_version,
        recommendations=recommendations,
    )


UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.get('/api/v1/match-runs/{match_run_id}', tags=['match-runs'], responses=UNIMPLEMENTED, status_code=501,
            **role_access(*READ_ROLES),
            description='Allowed roles: ADMIN, SUPERVISOR, VIEWER, within authorized run scope.')
def retrieve_match_run(match_run_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
