"""Deterministic ranking of scored snapshots, without HTTP or database access."""

from typing import Annotated

from pydantic import BaseModel, Field

from skillmatch.features.matching.canonical_scoring import ScoringResult
from skillmatch.features.matching.eligibility import EligibilityResult
from skillmatch.features.matching.schemas import Recommendation


class CandidateRankingInput(BaseModel):
    employee_id: Annotated[str, Field(min_length=1)]
    scoring: ScoringResult
    eligibility: EligibilityResult

    model_config = {'frozen': True, 'extra': 'forbid'}


class RankedCandidate(CandidateRankingInput):
    rank: Annotated[int, Field(ge=1)]


class _RankingOptions(BaseModel):
    minimum_score: Annotated[float, Field(ge=0, le=100)]
    max_results: Annotated[int, Field(ge=1, le=100, strict=True)]
    include_ineligible: Annotated[bool, Field(strict=True)]

    model_config = {'frozen': True, 'allow_inf_nan': False}


def rank_candidates(
    candidates: tuple[CandidateRankingInput, ...], *, minimum_score: float,
    max_results: int, include_ineligible: bool,
) -> tuple[RankedCandidate, ...]:
    """Filter, sort, and rank a single-model snapshot without mutating its evidence.

    Sort descending by unrounded score, required-skill coverage, and
    certification coverage, then ascending by employee ID. Absent categories
    contribute zero to their tie-break key. All candidates for a given job
    have the same absent categories. Filtering precedes truncation; returned
    ranks are contiguous and one-based.
    """
    options = _RankingOptions(minimum_score=minimum_score, max_results=max_results,
                              include_ineligible=include_ineligible)
    if len({item.employee_id for item in candidates}) != len(candidates):
        raise ValueError('Duplicate employee_id in ranking snapshot')
    if len({item.scoring.model_version for item in candidates}) > 1:
        raise ValueError('Ranking snapshot must use one model_version')
    selected = sorted(
        (item for item in candidates
         if (item.eligibility.eligible or options.include_ineligible)
         and item.scoring.score >= options.minimum_score),
        key=lambda item: (-item.scoring.score, -(item.scoring.required_skills or 0.0),
                          -(item.scoring.required_certifications or 0.0), item.employee_id),
    )[:options.max_results]
    return tuple(
        RankedCandidate(employee_id=item.employee_id, scoring=item.scoring,
                        eligibility=item.eligibility, rank=index)
        for index, item in enumerate(selected, start=1)
    )


def rank_recommendations(
    recommendations: list[Recommendation], minimum_score: float, top_k: int,
) -> list[Recommendation]:
    """Apply the same ordering to the active legacy recommendation API.

    For a fixed job, legacy weighted R/C contributions preserve the ordering
    of their respective coverage values. Legacy score generation is unchanged.
    """
    return sorted(
        (item for item in recommendations if item.score >= minimum_score),
        key=lambda item: (-item.score, -item.score_breakdown.required_skills,
                          -item.score_breakdown.required_certifications, item.employee_id),
    )[:top_k]
