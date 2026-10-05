from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class EmployeeSkill(BaseModel):
    skill_id: str
    proficiency: Annotated[int, Field(ge=1, le=5)]
    years_experience: Annotated[float, Field(ge=0)] = 0.0
    last_used_on: date | None = None


class EmployeeCertification(BaseModel):
    code: str
    name: str = ""
    issuer: str = ""
    issued_on: date
    expires_on: date | None = None


class Employee(BaseModel):
    id: str
    name: str
    skills: list[str]
    certifications: list[str]
    years_experience: Annotated[float, Field(ge=0)]
    status: Literal["ACTIVE", "INACTIVE"] = "ACTIVE"
    skill_evidence: list[EmployeeSkill] = Field(default_factory=list)
    certification_evidence: list[EmployeeCertification] = Field(default_factory=list)


# Section 6 contracts; the alpha Employee schema remains supported above.

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
