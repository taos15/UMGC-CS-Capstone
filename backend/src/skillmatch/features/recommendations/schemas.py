from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from skillmatch.features.matching.schemas import CandidateResult, Recommendation


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


class RecommendationResponse(BaseModel):
    job_id: str = Field(alias="jobId")
    recommendations: list[Recommendation]

    model_config = {"populate_by_name": True}


class RecommendationOptions(BaseModel):
    max_results: Annotated[int, Field(ge=1, le=100)]
    minimum_score: Annotated[float, Field(ge=0, le=100)]
    include_ineligible: bool


class MatchRun(BaseModel):
    match_run_id: str
    job_id: str
    requested_by: str
    model_version: str
    snapshot_hash: str
    options: RecommendationOptions
    generated_at: datetime
    results: list[CandidateResult]
