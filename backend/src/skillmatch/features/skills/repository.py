from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from skillmatch.db.conflicts import DuplicateKey
from skillmatch.features.skills.models import SkillRecord


def list_skills(session: Session, page: int, page_size: int) -> list[str]:
    return [row.skill_id for row in session.exec(select(SkillRecord).order_by(SkillRecord.skill_id)
            .offset((page - 1) * page_size).limit(page_size))]


def create_skill(session: Session, skill_id: str) -> str:
    try:
        session.add(SkillRecord(skill_id=skill_id))
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateKey from None
    return skill_id


def unknown_skills(session: Session, skill_ids: list[str]) -> list[str]:
    known = set(session.exec(select(SkillRecord.skill_id).where(SkillRecord.skill_id.in_(skill_ids))))
    return sorted(set(skill_ids) - known)
