"""Database-backed jobs, including compare-and-swap writes."""
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from skillmatch.db import session as database
from skillmatch.db.conflicts import RecordMissing, StaleVersion, DuplicateKey
from skillmatch.features.jobs.models import JobRecord
from skillmatch.features.jobs.schemas import JobProfile, Job


def get_profile(record_id: str, session: Session | None = None) -> JobProfile | None:
    if session is None:
        with Session(database.engine) as owned:
            return get_profile(record_id, owned)
    row = session.get(JobRecord, record_id)
    return JobProfile.model_validate({**row.payload, 'id': row.id, 'version': row.version}) if row else None


def list_profiles(page: int = 1, page_size: int = 25, session: Session | None = None) -> list[JobProfile]:
    if session is None:
        with Session(database.engine) as owned:
            return list_profiles(page, page_size, owned)
    rows = session.exec(select(JobRecord).order_by(JobRecord.job_code).offset((page-1)*page_size).limit(page_size))
    return [JobProfile.model_validate({**row.payload, 'id': row.id, 'version': row.version}) for row in rows]


def create_profile(session: Session, profile: JobProfile) -> JobProfile:
    row = JobRecord(id=profile.id, job_code=profile.job_code, version=1, payload=profile.model_dump(mode='json'))
    try:
        session.add(row)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateKey from None
    return profile


def update_profile(session: Session, profile: JobProfile) -> JobProfile:
    revised = profile.model_copy(update={'version': profile.version + 1})
    try:
        result = session.execute(update(JobRecord).where(
            JobRecord.id == profile.id, JobRecord.version == profile.version,
        ).values(job_code=profile.job_code, version=revised.version, payload=revised.model_dump(mode='json')))
        if result.rowcount != 1:
            exists = session.get(JobRecord, profile.id) is not None
            session.rollback()
            raise StaleVersion if exists else RecordMissing
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateKey from None
    return revised


def delete_profile(session: Session, record_id: str, version: int) -> None:
    result = session.execute(delete(JobRecord).where(JobRecord.id == record_id, JobRecord.version == version))
    if result.rowcount != 1:
        exists = session.get(JobRecord, record_id) is not None
        session.rollback()
        raise StaleVersion if exists else RecordMissing
    session.commit()


def to_matching(profile: JobProfile) -> Job:
    return Job(id=profile.id, title=profile.title, status='OPEN' if profile.status == 'OPEN' else 'CLOSED',
        minimum_years_experience=profile.minimum_years_experience,
        required_skills=[item.skill_id for item in profile.skill_requirements if item.level == 'REQUIRED'],
        preferred_skills=[item.skill_id for item in profile.skill_requirements if item.level == 'PREFERRED'],
        required_certifications=profile.certification_requirements, skill_requirement_details=profile.skill_requirements)


def get_job(job_id: str) -> Job | None:
    profile = get_profile(job_id)
    return to_matching(profile) if profile else None
