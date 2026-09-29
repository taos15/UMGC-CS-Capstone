from typing import Annotated

from pydantic import BaseModel, Field


class Job(BaseModel):
    id: str
    title: str
    required_skills: list[str]
    preferred_skills: list[str] = Field(default_factory=list)
    required_certifications: list[str]
    minimum_years_experience: Annotated[float, Field(ge=0)]
