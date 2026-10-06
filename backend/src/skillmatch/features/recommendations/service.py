"""Recommendation orchestrator: snapshot -> matching -> persistence (REC-001).

Owns auth context, snapshots, repository calls, matching invocation, and
match-run persistence, per the Recommendation Orchestrator responsibility row
in resources/spec_bundle/project/project_design_contract.md.
"""

import hashlib
import json
from datetime import date

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from skillmatch.core.errors import ProblemError
from skillmatch.features.employees.repository import get_employees
from skillmatch.features.employees.schemas import Employee
from skillmatch.features.jobs.schemas import Job
from skillmatch.features.matching.canonical_scoring import (
    EmployeeScoringInput,
    JobScoringInput,
    SkillProficiency,
    SkillRequirement,
    score_candidate,
)
from skillmatch.features.matching.eligibility import (
    CertificationEvidence,
    EmployeeEligibilityInput,
    evaluate_eligibility,
)
from skillmatch.features.matching.explanations import build_candidate_result
from skillmatch.features.matching.ranking import CandidateRankingInput, rank_candidates
from skillmatch.features.matching.schemas import CandidateResult
from skillmatch.features.recommendations.repository import create_match_run

MODEL_VERSION = "rpce-55-20-15-10-v1"


def _job_scoring_input(job: Job) -> JobScoringInput:
    try:
        return JobScoringInput(
            skill_requirements=tuple(
                SkillRequirement(
                    skill_id=requirement.skill_id,
                    level=requirement.level,
                    minimum_proficiency=requirement.minimum_proficiency,
                    importance=requirement.importance,
                )
                for requirement in job.skill_requirement_details
            ),
            required_certification_codes=frozenset(job.required_certifications),
            minimum_years_experience=job.minimum_years_experience,
        )
    except ValueError:
        raise ProblemError(
            422, "JOB_HAS_NO_CRITERIA", "Job has no usable matching criteria."
        ) from None


def _eligibility_input(employee: Employee) -> EmployeeEligibilityInput:
    return EmployeeEligibilityInput(
        status=employee.status,
        certifications=tuple(
            CertificationEvidence(
                code=evidence.code,
                issued_on=evidence.issued_on,
                expires_on=evidence.expires_on,
            )
            for evidence in employee.certification_evidence
        ),
    )


def _snapshot_hash(job: Job, employees: list[Employee], options: dict, as_of: date) -> str:
    payload = json.dumps({
        'job': job.model_dump(mode='json'),
        'employees': [employee.model_dump(mode='json') for employee in sorted(employees, key=lambda item: item.id)],
        'options': options, 'as_of': as_of.isoformat(), 'model_version': MODEL_VERSION,
    }, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()


def generate_recommendations(
    session: Session,
    job: Job,
    *,
    requested_by: str,
    candidate_employee_ids: list[str] | None,
    top_k: int,
    minimum_score: float,
    include_missing_skills: bool,
    include_ineligible: bool,
) -> tuple[str, str, list[CandidateResult]]:
    if job.status != "OPEN":
        raise ProblemError(409, "JOB_NOT_OPEN", "Job is not open for recommendations.")

    job_input = _job_scoring_input(job)

    try:
        active_employees = [
            employee
            for employee in get_employees(candidate_employee_ids)
            if employee.status == "ACTIVE"
        ]
    except SQLAlchemyError:
        raise ProblemError(503, 'DATABASE_UNAVAILABLE', 'Recommendations are temporarily unavailable.') from None

    try:
        as_of = date.today()
        ranking_inputs: list[CandidateRankingInput] = []
        employees_by_id: dict[str, Employee] = {}
        for employee in active_employees:
            eligibility = evaluate_eligibility(_eligibility_input(employee), job_input, as_of=as_of)
            proficiencies = {
                evidence.skill_id: evidence.proficiency for evidence in employee.skill_evidence
            }
            scoring_input = EmployeeScoringInput(
                skills=tuple(
                    SkillProficiency(skill_id=skill_id, proficiency=proficiency)
                    for skill_id, proficiency in proficiencies.items()
                ),
                valid_certification_codes=eligibility.valid_certification_codes,
                total_years_experience=employee.years_experience,
            )
            scoring = score_candidate(scoring_input, job_input)
            ranking_inputs.append(
                CandidateRankingInput(employee_id=employee.id, scoring=scoring, eligibility=eligibility)
            )
            employees_by_id[employee.id] = employee

        ranked = rank_candidates(
            tuple(ranking_inputs),
            minimum_score=minimum_score,
            max_results=top_k,
            include_ineligible=include_ineligible,
        )

        results = [
            build_candidate_result(
                employee_id=item.employee_id,
                employee_name=employees_by_id[item.employee_id].name,
                job_title=job.title,
                proficiencies={
                    evidence.skill_id: evidence.proficiency
                    for evidence in employees_by_id[item.employee_id].skill_evidence
                },
                job=job_input,
                scoring=item.scoring,
                eligibility=item.eligibility,
                rank=item.rank,
                include_missing_skills=include_missing_skills,
            )
            for item in ranked
        ]
    except Exception:
        raise ProblemError(503, 'MATCH_ENGINE_UNAVAILABLE', 'Matching is temporarily unavailable.') from None

    options = {
        "topK": top_k,
        "minimumScore": minimum_score,
        "includeMissingSkills": include_missing_skills,
        "includeIneligible": include_ineligible,
    }
    snapshot_hash = _snapshot_hash(
        job, active_employees, options, as_of
    )

    try:
        match_run = create_match_run(
            session,
            job_id=job.id,
            requested_by=requested_by,
            model_version=MODEL_VERSION,
            snapshot_hash=snapshot_hash,
            options=options,
            results=[result.model_dump() for result in results],
        )
    except Exception as error:
        session.rollback()
        raise ProblemError(
            503, "DATABASE_UNAVAILABLE", "Recommendations are temporarily unavailable."
        ) from error

    return match_run.match_run_id, MODEL_VERSION, results
