"""Versioned R/P/C/E scoring, independent of the legacy recommendation API."""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator


class _FrozenModel(BaseModel):
    model_config = {"frozen": True, "extra": "forbid", "allow_inf_nan": False}


class SkillProficiency(_FrozenModel):
    skill_id: Annotated[str, Field(min_length=1)]
    proficiency: Annotated[int, Field(ge=1, le=5, strict=True)]


class SkillRequirement(_FrozenModel):
    skill_id: Annotated[str, Field(min_length=1)]
    level: Literal["REQUIRED", "PREFERRED"]
    minimum_proficiency: Annotated[int, Field(ge=1, le=5, strict=True)]
    importance: Annotated[int, Field(ge=1, le=3, strict=True)]


class EmployeeScoringInput(_FrozenModel):
    skills: tuple[SkillProficiency, ...]
    # The caller resolves validity at a fixed snapshot, excluding expired credentials.
    valid_certification_codes: frozenset[Annotated[str, Field(min_length=1)]]
    total_years_experience: Annotated[float, Field(ge=0)]

    @field_validator("skills")
    @classmethod
    def unique_skills(cls, skills: tuple[SkillProficiency, ...]) -> tuple[SkillProficiency, ...]:
        if len({skill.skill_id for skill in skills}) != len(skills):
            raise ValueError("Duplicate skill_id in employee skills")
        return skills


class JobScoringInput(_FrozenModel):
    skill_requirements: tuple[SkillRequirement, ...]
    required_certification_codes: frozenset[Annotated[str, Field(min_length=1)]]
    minimum_years_experience: Annotated[float, Field(ge=0)]

    @model_validator(mode="after")
    def usable_unique_criteria(self) -> Self:
        if len({skill.skill_id for skill in self.skill_requirements}) != len(self.skill_requirements):
            raise ValueError("Duplicate skill_id in job requirements")
        if not (self.skill_requirements or self.required_certification_codes or self.minimum_years_experience > 0):
            raise ValueError("Job must have at least one usable scoring criterion")
        return self


class ScoringResult(_FrozenModel):
    model_version: Literal["rpce-55-20-15-10-v1"] = "rpce-55-20-15-10-v1"
    required_skills: float | None
    preferred_skills: float | None
    required_certifications: float | None
    experience: float
    score: float


def _skill_coverage(
    proficiencies: dict[str, int],
    requirements: tuple[SkillRequirement, ...],
    level: Literal["REQUIRED", "PREFERRED"],
) -> float | None:
    selected = [requirement for requirement in requirements if requirement.level == level]
    if not selected:
        return None
    return sum(
        requirement.importance
        * min(proficiencies.get(requirement.skill_id, 0) / requirement.minimum_proficiency, 1.0)
        for requirement in selected
    ) / sum(requirement.importance for requirement in selected)


def score_candidate(employee: EmployeeScoringInput, job: JobScoringInput) -> ScoringResult:
    """Return unrounded components and a 0-100 score from a validated snapshot.

    Missing skills contribute zero. Absent R/P/C categories are omitted from
    the denominator; E always participates, including when its minimum is zero.
    Certification validity is supplied by the caller, not inferred here.
    """
    proficiencies = {skill.skill_id: skill.proficiency for skill in employee.skills}
    required = _skill_coverage(proficiencies, job.skill_requirements, "REQUIRED")
    preferred = _skill_coverage(proficiencies, job.skill_requirements, "PREFERRED")
    certifications = (
        len(employee.valid_certification_codes & job.required_certification_codes)
        / len(job.required_certification_codes)
        if job.required_certification_codes else None
    )
    experience = (
        min(employee.total_years_experience / job.minimum_years_experience, 1.0)
        if job.minimum_years_experience else 1.0
    )
    # These weights belong to rpce-55-20-15-10-v1; changes require a new version.
    components = ((required, 55), (preferred, 20), (certifications, 15), (experience, 10))
    present = [(value, weight) for value, weight in components if value is not None]
    score = 100 * sum(value * weight for value, weight in present) / sum(weight for _, weight in present)
    return ScoringResult(
        required_skills=required,
        preferred_skills=preferred,
        required_certifications=certifications,
        experience=experience,
        score=score,
    )
