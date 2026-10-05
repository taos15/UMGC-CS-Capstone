"""Approved stored-run scope, shared by retrieval and feedback."""

from skillmatch.core.errors import ProblemError
from skillmatch.features.auth.schemas import AuthenticatedUser
from skillmatch.features.recommendations.models import MatchRun


def authorize_match_run(user: AuthenticatedUser, run: MatchRun) -> None:
    if user.role != 'ADMIN' and run.requested_by != str(user.user_id):
        raise ProblemError(403, 'FORBIDDEN', 'You do not have permission to perform this action.')
