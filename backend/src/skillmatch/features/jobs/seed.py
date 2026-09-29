"""Transitional in-memory job seed data."""

from skillmatch.features.jobs.schemas import Job


JOBS = [
    Job(
        id="job-electrician",
        title="Commercial Electrician",
        required_skills=["electrical wiring", "blueprint reading", "troubleshooting"],
        preferred_skills=["project coordination"],
        required_certifications=["licensed electrician"],
        minimum_years_experience=5,
    ),
    Job(
        id="job-hvac",
        title="HVAC Technician",
        required_skills=["hvac repair", "troubleshooting"],
        required_certifications=["epa 608"],
        minimum_years_experience=3,
    ),
]
