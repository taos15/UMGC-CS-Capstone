from typing import Annotated
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from skillmatch.core.errors import ProblemError
from skillmatch.db.session import get_db
from skillmatch.db.conflicts import DuplicateKey
from skillmatch.features.auth.dependencies import READ_ROLES, ADMIN_ROLES, role_access
from skillmatch.features.skills.repository import list_skills, create_skill

router = APIRouter()


class SkillCreate(BaseModel):
    model_config = {'extra': 'forbid'}
    skill_id: Annotated[str, Field(min_length=1, max_length=128)]

    @field_validator('skill_id')
    @classmethod
    def nonblank(cls, value):
        if not value.strip() or value != value.strip():
            raise ValueError('Skill ID must be nonblank without surrounding whitespace')
        return value


@router.get('/api/v1/skills', response_model=list[str], **role_access(*READ_ROLES))
def list_taxonomy(session: Annotated[Session, Depends(get_db)],
                  page: Annotated[int, Query(ge=1)] = 1,
                  page_size: Annotated[int, Query(ge=1, le=100)] = 25):
    try:
        return list_skills(session, page, page_size)
    except SQLAlchemyError:
        session.rollback()
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Skills are temporarily unavailable.') from None


@router.post('/api/v1/skills', response_model=str, status_code=201, **role_access(*ADMIN_ROLES))
def create_taxonomy(request: SkillCreate, session: Annotated[Session, Depends(get_db)]):
    try:
        return create_skill(session, request.skill_id)
    except DuplicateKey:
        raise ProblemError(409, 'SKILL_EXISTS', 'Skill already exists.') from None
    except SQLAlchemyError:
        session.rollback()
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Skills are temporarily unavailable.') from None
