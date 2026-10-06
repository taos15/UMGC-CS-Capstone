from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

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
    MatchRun,
    RecommendationRequest,
    RecommendationResponse,
)
from skillmatch.features.recommendations.access import authorize_match_run
from skillmatch.features.recommendations.service import generate_recommendations
from skillmatch.features.recommendations.repository import get_match_run, build_match_run_snapshot


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
    try:
        job = get_job(job_id)
    except SQLAlchemyError:
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Recommendations are temporarily unavailable.') from None
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


@router.get(
    '/api/v1/match-runs/{match_run_id}', tags=['match-runs'], response_model=MatchRun,
    responses={
        status: {'description': description, 'content': {'application/problem+json': {
            'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}
        for status, description in [(403, 'Run outside caller scope'),
                                    (404, 'Match run not found'),
                                    (503, 'Persistence unavailable')]
    },
    **role_access(*READ_ROLES),
    description='ADMIN can read all runs; SUPERVISOR and VIEWER can read their own runs. Returns stored evidence without recomputing.',
)
def retrieve_match_run(
    match_run_id: str,
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
) -> MatchRun:
    try:
        stored = get_match_run(session, match_run_id)
        if stored is None:
            raise ProblemError(404, 'MATCH_RUN_NOT_FOUND', 'Match run not found.')
        authorize_match_run(user, stored)
        return build_match_run_snapshot(session, stored)
    except SQLAlchemyError:
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Match runs are temporarily unavailable.') from None
