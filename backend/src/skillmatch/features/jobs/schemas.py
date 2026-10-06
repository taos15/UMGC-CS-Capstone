from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


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


class JobCreate(BaseModel):
    model_config = {'extra': 'forbid'}
    job_code: Annotated[str, Field(min_length=1, max_length=128)]
    title: Annotated[str, Field(min_length=1, max_length=200)]
    description: str
    status: Literal['OPEN', 'CLOSED']
    minimum_years_experience: Annotated[float, Field(ge=0, allow_inf_nan=False)]
    skill_requirements: list[JobSkillRequirement]
    certification_requirements: list[str]

    @model_validator(mode='after')
    def unique_requirements(self):
        if len({item.skill_id for item in self.skill_requirements}) != len(self.skill_requirements):
            raise ValueError('Duplicate skill_id')
        return self


class JobUpdate(JobCreate):
    version: Annotated[int, Field(ge=1, strict=True)]
