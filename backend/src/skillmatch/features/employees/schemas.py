from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: str
    name: str
    skills: list[str]
    certifications: list[str]
    years_experience: Annotated[float, Field(ge=0)]


# Section 6 contracts; the alpha Employee schema remains supported above.

class EmployeeSkill(BaseModel):
    skill_id: str
    proficiency: Annotated[int, Field(ge=1, le=5)]
    years_experience: Annotated[float, Field(ge=0)]
    last_used_on: date | None = None


class EmployeeCertification(BaseModel):
    code: str
    name: str
    issuer: str
    issued_on: date
    expires_on: date | None = None


class EmployeeProfile(BaseModel):
    id: str
    employee_number: str
    name: str
    current_title: str
    status: str
    total_years_experience: Annotated[float, Field(ge=0)]
    version: int
    skills: list[EmployeeSkill]
    certifications: list[EmployeeCertification]
