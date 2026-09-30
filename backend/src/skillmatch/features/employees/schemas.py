from typing import Annotated

from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: str
    name: str
    skills: list[str]
    certifications: list[str]
    years_experience: Annotated[float, Field(ge=0)]
