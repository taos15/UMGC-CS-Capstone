"""Score the versioned mock profiles through the real pure matching engine."""
import argparse
import json
from datetime import date
from pathlib import Path

from skillmatch.features.employees.schemas import EmployeeProfile
from skillmatch.features.jobs.schemas import JobProfile
from skillmatch.features.matching.canonical_scoring import EmployeeScoringInput, JobScoringInput, SkillProficiency, SkillRequirement, score_candidate
from skillmatch.features.matching.eligibility import CertificationEvidence, EmployeeEligibilityInput, evaluate_eligibility
from skillmatch.features.matching.ranking import CandidateRankingInput, rank_candidates

DATA = Path(__file__).resolve().parents[1] / 'data' / 'mock'
AS_OF = date(2026, 10, 5)


def build_preview(as_of: date = AS_OF) -> dict:
    employees = [EmployeeProfile.model_validate(record) for record in json.loads((DATA / 'employees.json').read_text())]
    jobs = [JobProfile.model_validate(record) for record in json.loads((DATA / 'jobs.json').read_text())]
    preview = {'as_of': as_of.isoformat(), 'model_version': 'rpce-55-20-15-10-v1', 'jobs': []}
    by_id = {employee.id: employee for employee in employees}
    for job in jobs:
        job_input = JobScoringInput(
            skill_requirements=tuple(SkillRequirement(**item.model_dump()) for item in job.skill_requirements),
            required_certification_codes=frozenset(job.certification_requirements),
            minimum_years_experience=job.minimum_years_experience,
        )
        inputs = []
        for employee in employees:
            eligibility = evaluate_eligibility(EmployeeEligibilityInput(
                status=employee.status,
                certifications=tuple(CertificationEvidence(code=cert.code, issued_on=cert.issued_on, expires_on=cert.expires_on) for cert in employee.certifications),
            ), job_input, as_of=as_of)
            scoring = score_candidate(EmployeeScoringInput(
                skills=tuple(SkillProficiency(skill_id=skill.skill_id, proficiency=skill.proficiency) for skill in employee.skills),
                valid_certification_codes=eligibility.valid_certification_codes,
                total_years_experience=employee.total_years_experience,
            ), job_input)
            inputs.append(CandidateRankingInput(employee_id=employee.id, scoring=scoring, eligibility=eligibility))
        ranked = rank_candidates(tuple(inputs), minimum_score=0, max_results=100, include_ineligible=True)
        preview['jobs'].append({'job_code': job.job_code, 'title': job.title, 'candidates': [
            {'employee_number': by_id[item.employee_id].employee_number, 'name': by_id[item.employee_id].name,
             'rank': item.rank, 'score': round(item.scoring.score, 2), 'eligible': item.eligibility.eligible,
             'ineligible_reasons': list(item.eligibility.ineligible_reasons)} for item in ranked
        ]})
    return preview


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of', type=date.fromisoformat, default=AS_OF)
    args = parser.parse_args()
    print(json.dumps(build_preview(args.as_of), indent=2))
