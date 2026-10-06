from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


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


class EmployeeCreate(BaseModel):
    model_config = {'extra': 'forbid'}
    employee_number: Annotated[str, Field(min_length=1, max_length=128)]
    name: Annotated[str, Field(min_length=1, max_length=200)]
    current_title: str
    status: Literal['ACTIVE', 'INACTIVE']
    total_years_experience: Annotated[float, Field(ge=0, allow_inf_nan=False)]
    skills: list[EmployeeSkill]
    certifications: list[EmployeeCertification]

    @model_validator(mode="after")
    def validate_evidence(self):
        if len({item.skill_id for item in self.skills}) != len(self.skills):
            raise ValueError('Duplicate skill_id')
        for item in self.certifications:
            if item.expires_on is not None and item.expires_on < item.issued_on:
                raise ValueError('Certification expires before issue date')
        return self


class EmployeeUpdate(EmployeeCreate):
    version: Annotated[int, Field(ge=1, strict=True)]
