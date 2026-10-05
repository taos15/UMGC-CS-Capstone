"""Transitional in-memory job seed data."""

from skillmatch.features.jobs.schemas import Job, JobSkillRequirement


JOBS = [
    Job(
        id="job-electrician",
        title="Commercial Electrician",
        required_skills=["electrical wiring", "blueprint reading", "troubleshooting"],
        preferred_skills=["project coordination"],
        required_certifications=["licensed electrician"],
        minimum_years_experience=5,
        status="OPEN",
        skill_requirement_details=[
            JobSkillRequirement(skill_id="electrical wiring", level="REQUIRED",
                                 minimum_proficiency=3, importance=3),
            JobSkillRequirement(skill_id="blueprint reading", level="REQUIRED",
                                 minimum_proficiency=3, importance=2),
            JobSkillRequirement(skill_id="troubleshooting", level="REQUIRED",
                                 minimum_proficiency=3, importance=2),
            JobSkillRequirement(skill_id="project coordination", level="PREFERRED",
                                 minimum_proficiency=3, importance=1),
        ],
    ),
    Job(
        id="job-hvac",
        title="HVAC Technician",
        required_skills=["hvac repair", "troubleshooting"],
        required_certifications=["epa 608"],
        minimum_years_experience=3,
        status="OPEN",
        skill_requirement_details=[
            JobSkillRequirement(skill_id="hvac repair", level="REQUIRED",
                                 minimum_proficiency=3, importance=3),
            JobSkillRequirement(skill_id="troubleshooting", level="REQUIRED",
                                 minimum_proficiency=3, importance=2),
        ],
    ),
]
