"""Canonical profile endpoints; roles are enforced before repository access."""
from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from skillmatch.core.errors import ProblemError
from skillmatch.db.session import get_db
from skillmatch.db.conflicts import DuplicateKey, RecordMissing, StaleVersion
from skillmatch.features.auth.dependencies import ADMIN_ROLES, READ_ROLES, role_access
from skillmatch.features.jobs import repository
from skillmatch.features.jobs.schemas import JobProfile, JobCreate, JobUpdate

router = APIRouter()


class DeleteRequest(BaseModel):
    model_config = {'extra': 'forbid'}
    version: Annotated[int, Field(ge=1, strict=True)]


def perform(session, operation):
    try:
        return operation()
    except DuplicateKey:
        raise ProblemError(409, 'JOB_EXISTS', 'Job business identifier already exists.') from None
    except StaleVersion:
        raise ProblemError(409, 'STALE_VERSION', 'Profile version is out of date.') from None
    except RecordMissing:
        raise ProblemError(404, 'JOB_NOT_FOUND', 'Job not found.') from None
    except SQLAlchemyError:
        session.rollback()
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Profiles are temporarily unavailable.') from None


# Keep the read callable name available for instrumentation and failure tests.
get_jobs = repository.list_profiles


@router.get('/api/v1/jobs', response_model=list[JobProfile], **role_access(*READ_ROLES))
def list_jobs(session: Annotated[Session, Depends(get_db)],
                   page: Annotated[int, Query(ge=1)] = 1,
                   page_size: Annotated[int, Query(ge=1, le=100)] = 25):
    return perform(session, lambda: get_jobs(page=page, page_size=page_size, session=session))


@router.get('/api/v1/jobs/{job_id}', response_model=JobProfile, **role_access(*READ_ROLES))
def retrieve_profile(job_id: str, session: Annotated[Session, Depends(get_db)]):
    result = perform(session, lambda: repository.get_profile(job_id, session))
    if result is None:
        raise ProblemError(404, 'JOB_NOT_FOUND', 'Job not found.')
    return result


@router.post('/api/v1/jobs', response_model=JobProfile, status_code=201, **role_access(*ADMIN_ROLES))
def create_profile(request: JobCreate, session: Annotated[Session, Depends(get_db)]):
    validate_domain(request)
    validate_skills(session, request)
    profile = JobProfile(id=str(uuid4()), version=1, **request.model_dump())
    return perform(session, lambda: repository.create_profile(session, profile))


@router.put('/api/v1/jobs/{job_id}', response_model=JobProfile, **role_access(*ADMIN_ROLES))
def update_profile(job_id: str, request: JobUpdate, session: Annotated[Session, Depends(get_db)]):
    validate_domain(request)
    validate_skills(session, request)
    profile = JobProfile(id=job_id, **request.model_dump())
    return perform(session, lambda: repository.update_profile(session, profile))


@router.delete('/api/v1/jobs/{job_id}', status_code=204, **role_access(*ADMIN_ROLES))
def delete_profile(job_id: str, request: DeleteRequest, session: Annotated[Session, Depends(get_db)]):
    perform(session, lambda: repository.delete_profile(session, job_id, request.version))
    return Response(status_code=204)


def validate_domain(request):
    if request.status == "OPEN" and not (request.skill_requirements or request.certification_requirements or request.minimum_years_experience > 0):
        raise ProblemError(422, "JOB_HAS_NO_CRITERIA", "Job has no usable matching criteria.")


def validate_skills(session, request):
    from skillmatch.features.skills.repository import unknown_skills
    ids = [item.skill_id for item in request.skill_requirements]
    missing = perform(session, lambda: unknown_skills(session, ids))
    if missing:
        raise ProblemError(422, 'VALIDATION_ERROR', 'Profile references unknown skill IDs.')
