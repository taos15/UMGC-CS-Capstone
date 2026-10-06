"""Persist human decisions without staffing or live matching side effects."""

from datetime import timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from skillmatch.core.errors import ProblemError
from skillmatch.features.auth.schemas import AuthenticatedUser
from skillmatch.features.feedback.repository import create_feedback
from skillmatch.features.feedback.schemas import Feedback, FeedbackRequest
from skillmatch.features.recommendations.access import authorize_match_run
from skillmatch.features.recommendations.repository import get_candidate_results, get_match_run


def record_feedback(session: Session, run_id: str, user: AuthenticatedUser, request: FeedbackRequest) -> Feedback:
    try:
        run = get_match_run(session, run_id)
        if run is None:
            raise ProblemError(404, 'MATCH_RUN_NOT_FOUND', 'Match run not found.')
        authorize_match_run(user, run)
        if request.decision == 'SELECTED':
            candidate = next((result for result in get_candidate_results(session, run_id)
                              if result.employee_id == request.selected_employee_id), None)
            if candidate is None or not candidate.eligible:
                raise ProblemError(409, 'FEEDBACK_CONFLICT', 'Selected employee must be an eligible candidate in this match run.')
        saved = create_feedback(session, match_run_id=run_id, user_id=str(user.user_id), **request.model_dump())
        created_at = saved.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        return Feedback(**{**saved.model_dump(), 'created_at': created_at.astimezone(timezone.utc)})
    except SQLAlchemyError:
        session.rollback()
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Feedback is temporarily unavailable.') from None
