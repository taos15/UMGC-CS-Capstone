from app.schemas import Employee, Job


EMPLOYEES = [
    Employee(
        id="emp-alex",
        name="Alex Morgan",
        skills=[
            "electrical wiring",
            "blueprint reading",
            "troubleshooting",
            "project coordination",
        ],
        certifications=["licensed electrician", "osha 10"],
        years_experience=8,
    ),
    Employee(
        id="emp-jordan",
        name="Jordan Lee",
        skills=["electrical wiring", "troubleshooting", "project coordination"],
        certifications=["osha 10"],
        years_experience=4,
    ),
    Employee(
        id="emp-sam",
        name="Sam Rivera",
        skills=["hvac repair", "troubleshooting", "customer service"],
        certifications=["epa 608"],
        years_experience=6,
    ),
]

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
