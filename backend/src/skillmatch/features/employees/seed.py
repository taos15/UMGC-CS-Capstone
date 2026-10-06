"""Transitional in-memory employee seed data."""

from skillmatch.features.employees.schemas import (
    Employee,
    EmployeeCertification,
    EmployeeSkill,
)


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
        status="ACTIVE",
        skill_evidence=[
            EmployeeSkill(skill_id="electrical wiring", proficiency=5, years_experience=8),
            EmployeeSkill(skill_id="blueprint reading", proficiency=5, years_experience=6),
            EmployeeSkill(skill_id="troubleshooting", proficiency=5, years_experience=8),
            EmployeeSkill(skill_id="project coordination", proficiency=4, years_experience=4),
        ],
        certification_evidence=[
            EmployeeCertification(
                code="licensed electrician", name="Licensed Electrician",
                issuer="State Board", issued_on="2019-01-01",
            ),
            EmployeeCertification(
                code="osha 10", name="OSHA 10", issuer="OSHA",
                issued_on="2020-01-01",
            ),
        ],
    ),
    Employee(
        id="emp-jordan",
        name="Jordan Lee",
        skills=["electrical wiring", "troubleshooting", "project coordination"],
        certifications=["osha 10"],
        years_experience=4,
        status="ACTIVE",
        skill_evidence=[
            EmployeeSkill(skill_id="electrical wiring", proficiency=4, years_experience=4),
            EmployeeSkill(skill_id="troubleshooting", proficiency=3, years_experience=4),
            EmployeeSkill(skill_id="project coordination", proficiency=3, years_experience=2),
        ],
        certification_evidence=[
            EmployeeCertification(
                code="osha 10", name="OSHA 10", issuer="OSHA",
                issued_on="2021-01-01",
            ),
        ],
    ),
    Employee(
        id="emp-sam",
        name="Sam Rivera",
        skills=["hvac repair", "troubleshooting", "customer service"],
        certifications=["epa 608"],
        years_experience=6,
        status="ACTIVE",
        skill_evidence=[
            EmployeeSkill(skill_id="hvac repair", proficiency=4, years_experience=6),
            EmployeeSkill(skill_id="troubleshooting", proficiency=4, years_experience=6),
            EmployeeSkill(skill_id="customer service", proficiency=3, years_experience=6),
        ],
        certification_evidence=[
            EmployeeCertification(
                code="epa 608", name="EPA 608", issuer="EPA",
                issued_on="2018-01-01",
            ),
        ],
    ),
]
