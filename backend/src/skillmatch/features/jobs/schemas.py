from typing import Annotated, Literal

from pydantic import BaseModel, Field


class JobSkillRequirement(BaseModel):
    skill_id: str
    level: Literal['REQUIRED', 'PREFERRED']
    minimum_proficiency: Annotated[int, Field(ge=1, le=5)]
    importance: Annotated[int, Field(ge=1, le=3)]


class Job(BaseModel):
    id: str
    title: str
    required_skills: list[str]
    preferred_skills: list[str] = Field(default_factory=list)
    required_certifications: list[str]
    minimum_years_experience: Annotated[float, Field(ge=0)]
    status: Literal['OPEN', 'CLOSED'] = 'OPEN'
    skill_requirement_details: list[JobSkillRequirement] = Field(default_factory=list)


class JobProfile(BaseModel):
    id: str
    job_code: str
    title: str
    description: str
    status: str
    minimum_years_experience: Annotated[float, Field(ge=0)]
    version: int
    skill_requirements: list[JobSkillRequirement]
    certification_requirements: list[str]
