"""Database-backed employees, including compare-and-swap writes."""
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from skillmatch.db import session as database
from skillmatch.db.conflicts import RecordMissing, StaleVersion, DuplicateKey
from skillmatch.features.employees.models import EmployeeRecord
from skillmatch.features.employees.schemas import EmployeeProfile, Employee


def get_profile(record_id: str, session: Session | None = None) -> EmployeeProfile | None:
    if session is None:
        with Session(database.engine) as owned:
            return get_profile(record_id, owned)
    row = session.get(EmployeeRecord, record_id)
    return EmployeeProfile.model_validate({**row.payload, 'id': row.id, 'version': row.version}) if row else None


def list_profiles(page: int = 1, page_size: int = 25, session: Session | None = None) -> list[EmployeeProfile]:
    if session is None:
        with Session(database.engine) as owned:
            return list_profiles(page, page_size, owned)
    rows = session.exec(select(EmployeeRecord).order_by(EmployeeRecord.employee_number).offset((page-1)*page_size).limit(page_size))
    return [EmployeeProfile.model_validate({**row.payload, 'id': row.id, 'version': row.version}) for row in rows]


def create_profile(session: Session, profile: EmployeeProfile) -> EmployeeProfile:
    row = EmployeeRecord(id=profile.id, employee_number=profile.employee_number, version=1, payload=profile.model_dump(mode='json'))
    try:
        session.add(row)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateKey from None
    return profile


def update_profile(session: Session, profile: EmployeeProfile) -> EmployeeProfile:
    revised = profile.model_copy(update={'version': profile.version + 1})
    try:
        result = session.execute(update(EmployeeRecord).where(
            EmployeeRecord.id == profile.id, EmployeeRecord.version == profile.version,
        ).values(employee_number=profile.employee_number, version=revised.version, payload=revised.model_dump(mode='json')))
        if result.rowcount != 1:
            exists = session.get(EmployeeRecord, profile.id) is not None
            session.rollback()
            raise StaleVersion if exists else RecordMissing
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateKey from None
    return revised


def delete_profile(session: Session, record_id: str, version: int) -> None:
    result = session.execute(delete(EmployeeRecord).where(EmployeeRecord.id == record_id, EmployeeRecord.version == version))
    if result.rowcount != 1:
        exists = session.get(EmployeeRecord, record_id) is not None
        session.rollback()
        raise StaleVersion if exists else RecordMissing
    session.commit()


def to_matching(profile: EmployeeProfile) -> Employee:
    return Employee(id=profile.id, name=profile.name, status='ACTIVE' if profile.status == 'ACTIVE' else 'INACTIVE',
        years_experience=profile.total_years_experience,
        skills=[item.skill_id for item in profile.skills], certifications=[item.code for item in profile.certifications],
        skill_evidence=profile.skills, certification_evidence=profile.certifications)


def get_employee(employee_id: str) -> Employee | None:
    profile = get_profile(employee_id)
    return to_matching(profile) if profile else None


def get_employees(employee_ids: list[str] | None = None) -> list[Employee]:
    with Session(database.engine) as session:
        query = select(EmployeeRecord).order_by(EmployeeRecord.employee_number)
        if employee_ids is not None:
            query = query.where(EmployeeRecord.id.in_(employee_ids))
        return [to_matching(EmployeeProfile.model_validate({**row.payload, 'id': row.id, 'version': row.version}))
                for row in session.exec(query)]
