from skillmatch.features.matching.explanations import build_explanation
from skillmatch.features.matching.schemas import (
    EmployeeInput,
    JobInput,
    Recommendation,
    ScoreBreakdown,
)


REQUIRED_SKILL_WEIGHT = 50
PREFERRED_SKILL_WEIGHT = 10
CERTIFICATION_WEIGHT = 25
EXPERIENCE_WEIGHT = 15


def build_recommendation(employee: EmployeeInput, job: JobInput) -> Recommendation:
    employee_skills = set(employee.skills)
    employee_certifications = set(employee.certifications)
    matched_skills = [
        skill for skill in job.required_skills if skill in employee_skills
    ]
    matched_preferred_skills = [
        skill for skill in job.preferred_skills if skill in employee_skills
    ]
    matched_certifications = [
        certification
        for certification in job.required_certifications
        if certification in employee_certifications
    ]
    missing_skills = [
        skill for skill in job.required_skills if skill not in employee_skills
    ]
    missing_certifications = [
        certification
        for certification in job.required_certifications
        if certification not in employee_certifications
    ]

    required_skill_score = _coverage_score(
        len(matched_skills), len(job.required_skills), REQUIRED_SKILL_WEIGHT
    )
    preferred_skill_score = _coverage_score(
        len(matched_preferred_skills),
        len(job.preferred_skills),
        PREFERRED_SKILL_WEIGHT,
    )
    certification_score = _coverage_score(
        len(matched_certifications),
        len(job.required_certifications),
        CERTIFICATION_WEIGHT,
    )
    experience_score = (
        EXPERIENCE_WEIGHT
        if employee.years_experience >= job.minimum_years_experience
        else EXPERIENCE_WEIGHT
        * employee.years_experience
        / job.minimum_years_experience
        if job.minimum_years_experience
        else EXPERIENCE_WEIGHT
    )
    missing_requirements = missing_skills + missing_certifications
    score_breakdown = ScoreBreakdown(
        requiredSkills=round(required_skill_score, 2),
        preferredSkills=round(preferred_skill_score, 2),
        requiredCertifications=round(certification_score, 2),
        experience=round(experience_score, 2),
    )
    return Recommendation(
        employeeId=employee.id,
        employeeName=employee.name,
        score=round(
            sum(
                (
                    score_breakdown.required_skills,
                    score_breakdown.preferred_skills,
                    score_breakdown.required_certifications,
                    score_breakdown.experience,
                )
            ),
            2,
        ),
        matchedSkills=matched_skills,
        matchedCertifications=matched_certifications,
        missingRequirements=missing_requirements,
        scoreBreakdown=score_breakdown,
        explanation=build_explanation(
            employee, job, matched_skills, matched_certifications, missing_requirements
        ),
    )


def _coverage_score(matched_count: int, required_count: int, weight: float) -> float:
    return weight if required_count == 0 else weight * matched_count / required_count
