from typing import Annotated

from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: str
    name: str
    skills: list[str]
    certifications: list[str]
    years_experience: Annotated[float, Field(ge=0)]


class Job(BaseModel):
    id: str
    title: str
    required_skills: list[str]
    preferred_skills: list[str] = Field(default_factory=list)
    required_certifications: list[str]
    minimum_years_experience: Annotated[float, Field(ge=0)]


class RecommendationRequest(BaseModel):
    candidate_employee_ids: list[str] | None = Field(
        default=None, alias="candidateEmployeeIds"
    )
    top_k: Annotated[int, Field(default=5, ge=1, le=100)] = Field(alias="topK")
    include_missing_skills: bool = Field(default=True, alias="includeMissingSkills")
    minimum_score: Annotated[float, Field(default=0.0, ge=0, le=100)] = Field(
        alias="minimumScore"
    )

    model_config = {"populate_by_name": True}


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


class RecommendationResponse(BaseModel):
    job_id: str = Field(alias="jobId")
    recommendations: list[Recommendation]

    model_config = {"populate_by_name": True}
