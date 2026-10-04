"""Persistence operations for supervisor feedback (DB-002)."""

from sqlmodel import Session, select

from skillmatch.features.feedback.models import Feedback


def create_feedback(
    session: Session,
    *,
    match_run_id: str,
    user_id: str,
    decision: str,
    selected_employee_id: str | None = None,
    rating: int | None = None,
    comment: str | None = None,
) -> Feedback:
    feedback = Feedback(
        match_run_id=match_run_id,
        user_id=user_id,
        decision=decision,
        selected_employee_id=selected_employee_id,
        rating=rating,
        comment=comment,
    )
    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback


def get_feedback_for_match_run(session: Session, match_run_id: str) -> list[Feedback]:
    statement = select(Feedback).where(Feedback.match_run_id == match_run_id)
    return list(session.exec(statement))
