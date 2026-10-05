from skillmatch.features.matching.canonical_scoring import JobScoringInput, ScoringResult
from skillmatch.features.matching.eligibility import EligibilityResult
from skillmatch.features.matching.schemas import CandidateResult, EmployeeInput, JobInput


def build_explanation(
    employee: EmployeeInput,
    job: JobInput,
    matched_skills: list[str],
    matched_certifications: list[str],
    missing_requirements: list[str],
) -> str:
    parts = [
        f"{employee.name} matches {len(matched_skills)} of {len(job.required_skills)} required skills",
        f"and holds {len(matched_certifications)} of {len(job.required_certifications)} required certifications.",
    ]
    if employee.years_experience >= job.minimum_years_experience:
        parts.append(
            f"Their {employee.years_experience:g} years of experience meets the "
            f"{job.minimum_years_experience:g}-year requirement."
        )
    else:
        parts.append(
            f"They have {employee.years_experience:g} years of experience, below the "
            f"{job.minimum_years_experience:g}-year requirement."
        )
    if missing_requirements:
        parts.append(f"Missing requirements: {', '.join(missing_requirements)}.")
    return " ".join(parts)


def build_candidate_result(
    *,
    employee_id: str,
    employee_name: str,
    job_title: str,
    proficiencies: dict[str, int],
    job: JobScoringInput,
    scoring: ScoringResult,
    eligibility: EligibilityResult,
    rank: int,
    include_missing_skills: bool,
) -> CandidateResult:
    """Assemble the public CandidateResult evidence/explanation for one ranked candidate.

    Only matching-owned types are accepted (no Employee/Job feature imports);
    the orchestrator extracts primitives from those models beforehand.
    """
    required = [req for req in job.skill_requirements if req.level == "REQUIRED"]
    matched_skills = [
        req.skill_id for req in required
        if proficiencies.get(req.skill_id, 0) >= req.minimum_proficiency
    ]
    missing_skills = [
        req.skill_id for req in required
        if proficiencies.get(req.skill_id, 0) < req.minimum_proficiency
    ]
    if not include_missing_skills:
        missing_skills = []

    component_scores = {
        name: value
        for name, value in (
            ("required_skills", scoring.required_skills),
            ("preferred_skills", scoring.preferred_skills),
            ("required_certifications", scoring.required_certifications),
            ("experience", scoring.experience),
        )
        if value is not None
    }

    parts = [f"{employee_name} scored {scoring.score:.2f} for {job_title}."]
    if eligibility.ineligible_reasons:
        parts.append(f"Ineligible: {', '.join(eligibility.ineligible_reasons)}.")
    if missing_skills:
        parts.append(f"Missing required skills: {', '.join(missing_skills)}.")
    if eligibility.missing_certifications:
        parts.append(
            f"Missing required certifications: {', '.join(eligibility.missing_certifications)}."
        )

    return CandidateResult(
        rank=rank,
        employee_id=employee_id,
        score=round(scoring.score, 2),
        eligible=eligibility.eligible,
        component_scores=component_scores,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        matched_certifications=list(eligibility.matched_certifications),
        missing_certifications=list(eligibility.missing_certifications),
        ineligible_reasons=list(eligibility.ineligible_reasons),
        explanation=" ".join(parts),
    )
