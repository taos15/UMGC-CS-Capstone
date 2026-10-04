from typing import Annotated

from pydantic import BaseModel, Field


class EmployeeInput(BaseModel):
    id: str
    name: str
    skills: tuple[str, ...]
    certifications: tuple[str, ...]
    years_experience: Annotated[float, Field(ge=0)]

    model_config = {"frozen": True}


class JobInput(BaseModel):
    id: str
    title: str
    required_skills: tuple[str, ...]
    preferred_skills: tuple[str, ...] = ()
    required_certifications: tuple[str, ...]
    minimum_years_experience: Annotated[float, Field(ge=0)]

    model_config = {"frozen": True}


class ScoreBreakdown(BaseModel):
    required_skills: float = Field(alias="requiredSkills")
    preferred_skills: float = Field(alias="preferredSkills")
    required_certifications: float = Field(alias="requiredCertifications")
    experience: float

    model_config = {"populate_by_name": True}


class Recommendation(BaseModel):
    employee_id: str = Field(alias="employeeId")
    employee_name: str = Field(alias="employeeName")
    score: float
    matched_skills: list[str] = Field(alias="matchedSkills")
    matched_certifications: list[str] = Field(alias="matchedCertifications")
    missing_requirements: list[str] = Field(alias="missingRequirements")
    score_breakdown: ScoreBreakdown = Field(alias="scoreBreakdown")
    explanation: str

    model_config = {"populate_by_name": True}


class CandidateResult(BaseModel):
    rank: Annotated[int, Field(ge=1)]
    employee_id: str
    score: Annotated[float, Field(ge=0, le=100)]
    eligible: bool
    component_scores: dict[str, float]
    matched_skills: list[str]
    missing_skills: list[str]
    matched_certifications: list[str]
    missing_certifications: list[str]
    ineligible_reasons: list[str]
    explanation: str
