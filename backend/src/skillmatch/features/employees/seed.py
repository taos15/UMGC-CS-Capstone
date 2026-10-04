"""Transitional in-memory employee seed data."""

from skillmatch.features.employees.schemas import Employee


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
