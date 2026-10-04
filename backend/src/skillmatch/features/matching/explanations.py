from skillmatch.features.matching.schemas import EmployeeInput, JobInput


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
