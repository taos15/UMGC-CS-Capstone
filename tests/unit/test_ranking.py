from itertools import permutations

import pytest
from pydantic import ValidationError

from skillmatch.features.matching.canonical_scoring import ScoringResult
from skillmatch.features.matching.eligibility import EligibilityResult
from skillmatch.features.matching.ranking import CandidateRankingInput, rank_candidates, rank_recommendations
from skillmatch.features.matching.schemas import Recommendation, ScoreBreakdown


def candidate(employee_id, score=80, required=0.8, certification=1.0, eligible=True):
    return CandidateRankingInput(
        employee_id=employee_id,
        scoring=ScoringResult(required_skills=required, preferred_skills=None,
                              required_certifications=certification, experience=1, score=score),
        eligibility=EligibilityResult(eligible=eligible, valid_certification_codes=frozenset(),
                                     matched_certifications=(), missing_certifications=(),
                                     ineligible_reasons=() if eligible else ('EMPLOYEE_NOT_ACTIVE',)),
    )


def rank(candidates, minimum_score=0, max_results=100, include_ineligible=False):
    return rank_candidates(tuple(candidates), minimum_score=minimum_score,
                           max_results=max_results, include_ineligible=include_ineligible)


def test_every_tie_break_and_input_permutation_reproduces_same_result():
    candidates = (
        candidate('final', score=90, required=0.1, certification=0.1),
        candidate('required', required=0.9, certification=0.1),
        candidate('certification', certification=1.0),
        candidate('a', certification=0.5), candidate('z', certification=0.5),
    )
    baseline = rank(candidates)
    assert [item.employee_id for item in baseline] == ['final', 'required', 'certification', 'a', 'z']
    assert [item.rank for item in baseline] == [1, 2, 3, 4, 5]
    for permutation in permutations(candidates):
        assert rank(permutation) == baseline
    assert [item.scoring.score for item in baseline] == [90, 80, 80, 80, 80]


def test_eligibility_threshold_and_limit_are_applied_before_return():
    candidates = (candidate('ineligible', score=100, eligible=False),
                  candidate('below', score=79), candidate('boundary', score=80), candidate('best', score=90))
    assert [item.employee_id for item in rank(candidates, minimum_score=80, max_results=1)] == ['best']
    assert [item.employee_id for item in rank(candidates, minimum_score=80)] == ['best', 'boundary']
    included = rank(candidates, minimum_score=80, max_results=2, include_ineligible=True)
    assert [item.employee_id for item in included] == ['ineligible', 'best']
    assert not included[0].eligibility.eligible
    assert included[0].eligibility.ineligible_reasons == ('EMPLOYEE_NOT_ACTIVE',)


def test_unrounded_scores_are_ranked_before_display_rounding():
    result = rank([candidate('a', score=80.00001, required=1), candidate('z', score=80.00002, required=0)])
    assert [item.employee_id for item in result] == ['z', 'a']


def test_absent_categories_and_complete_ties_use_employee_id():
    assert [item.employee_id for item in rank([candidate('z', required=None, certification=None),
                                             candidate('a', required=None, certification=None)])] == ['a', 'z']


def test_empty_and_all_filtered_results():
    assert rank([]) == ()
    assert rank([candidate('a', score=50)], minimum_score=51) == ()
    assert rank([candidate('a', eligible=False)]) == ()


def test_inputs_and_evidence_are_unchanged():
    candidates = (candidate('z'), candidate('a'))
    before = [item.model_dump() for item in candidates]
    ranked = rank(candidates)
    assert [item.model_dump() for item in candidates] == before
    with pytest.raises(ValidationError):
        ranked[0].rank = 99


@pytest.mark.parametrize('options', [
    {'minimum_score': -1}, {'minimum_score': 101}, {'minimum_score': float('nan')},
    {'max_results': 0}, {'max_results': 101}, {'max_results': 1.5},
])
def test_invalid_options_are_rejected(options):
    with pytest.raises(ValidationError):
        rank([candidate('a')], **options)


def test_duplicate_ids_and_mixed_model_versions_are_rejected():
    with pytest.raises(ValueError, match='Duplicate employee_id'):
        rank([candidate('same'), candidate('same', score=90)])
    first, second = candidate('a'), candidate('b')
    second = second.model_copy(update={'scoring': second.scoring.model_copy(update={'model_version': 'different-version'})})
    with pytest.raises(ValueError, match='model_version'):
        rank([first, second])


def test_legacy_recommendations_use_same_tie_break_order():
    def recommendation(employee_id, score, required, certification):
        return Recommendation(employee_id=employee_id, employee_name=employee_id, score=score,
                              matched_skills=[], matched_certifications=[], missing_requirements=[], explanation='Evidence',
                              score_breakdown=ScoreBreakdown(required_skills=required, preferred_skills=0,
                                                             required_certifications=certification, experience=0))
    candidates = [recommendation('z', 80, 40, 15), recommendation('a', 80, 40, 15),
                  recommendation('certification', 80, 40, 20), recommendation('required', 80, 45, 0),
                  recommendation('score', 90, 0, 0)]
    for permutation in permutations(candidates):
        result = rank_recommendations(list(permutation), minimum_score=80, top_k=5)
        assert [item.employee_id for item in result] == ['score', 'required', 'certification', 'a', 'z']


def test_scored_eligibility_snapshot_round_trip_reproduces_order_and_scores():
    from datetime import date
    from skillmatch.features.matching.canonical_scoring import (
        EmployeeScoringInput, JobScoringInput, SkillProficiency, SkillRequirement, score_candidate,
    )
    from skillmatch.features.matching.eligibility import EmployeeEligibilityInput, evaluate_eligibility
    job = JobScoringInput(
        skill_requirements=(SkillRequirement(skill_id='skill', level='REQUIRED', minimum_proficiency=4, importance=1),),
        required_certification_codes=frozenset(), minimum_years_experience=0,
    )
    snapshot = []
    for employee_id, status in [('z', 'ACTIVE'), ('a', 'ACTIVE'), ('inactive', 'INACTIVE')]:
        eligibility = evaluate_eligibility(EmployeeEligibilityInput(status=status, certifications=()), job, as_of=date(2026, 10, 4))
        scoring = score_candidate(EmployeeScoringInput(
            skills=(SkillProficiency(skill_id='skill', proficiency=4),),
            valid_certification_codes=eligibility.valid_certification_codes, total_years_experience=0,
        ), job)
        snapshot.append(CandidateRankingInput(employee_id=employee_id, scoring=scoring, eligibility=eligibility))
    baseline = rank(snapshot)
    restored = [CandidateRankingInput.model_validate_json(item.model_dump_json()) for item in snapshot[::-1]]
    assert rank(restored) == baseline
    assert [(item.rank, item.employee_id, item.scoring.score, item.scoring.model_version) for item in baseline] == [
        (1, 'a', 100, 'rpce-55-20-15-10-v1'), (2, 'z', 100, 'rpce-55-20-15-10-v1'),
    ]
