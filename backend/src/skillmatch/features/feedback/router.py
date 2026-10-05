"""Authenticated supervisor feedback; no automatic staffing decisions."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from skillmatch.db.session import get_db
from skillmatch.features.auth.dependencies import SUPERVISOR_ROLES, get_authenticated_user, role_access
from skillmatch.features.auth.schemas import AuthenticatedUser
from skillmatch.features.feedback.schemas import Feedback, FeedbackRequest
from skillmatch.features.feedback.service import record_feedback

router = APIRouter()


@router.post(
    '/api/v1/match-runs/{match_run_id}/feedback', tags=['feedback'],
    response_model=Feedback, status_code=201,
    responses={
        status: {'description': description, 'content': {'application/problem+json': {
            'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}
        for status, description in [(403, 'Caller lacks role or run scope'), (404, 'Match run not found'),
                                    (409, 'Selected candidate is invalid for this run'),
                                    (422, 'Invalid feedback fields'), (503, 'Persistence unavailable')]
    },
    **role_access(*SUPERVISOR_ROLES),
    description='ADMIN can record feedback on any run; SUPERVISOR on their own runs. Appends audit evidence without assigning employees or changing matching.',
)
def create_feedback(
    match_run_id: str,
    request: FeedbackRequest,
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
) -> Feedback:
    return record_feedback(session, match_run_id, user, request)
