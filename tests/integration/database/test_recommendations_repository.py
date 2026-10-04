from sqlmodel import Session, SQLModel, create_engine

from skillmatch.features.recommendations.repository import (
    create_match_run,
    get_candidate_results,
    get_match_run,
)


def _session() -> Session:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_create_match_run_persists_run_and_candidate_results() -> None:
    with _session() as session:
        match_run = create_match_run(
            session,
            job_id="job-electrician",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="abc123",
            options={"topK": 5, "minimumScore": 0.0},
            results=[
                {
                    "rank": 1,
                    "employee_id": "emp-alex",
                    "score": 95.0,
                    "eligible": True,
                    "component_scores": {"required_skills": 55.0},
                    "matched_skills": ["electrical wiring"],
                    "missing_skills": [],
                    "matched_certifications": ["licensed electrician"],
                    "missing_certifications": [],
                    "ineligible_reasons": [],
                    "explanation": "Strong match.",
                },
                {
                    "rank": 2,
                    "employee_id": "emp-jordan",
                    "score": 70.0,
                    "eligible": True,
                    "component_scores": {"required_skills": 40.0},
                    "matched_skills": ["electrical wiring"],
                    "missing_skills": ["blueprint reading"],
                    "matched_certifications": [],
                    "missing_certifications": ["licensed electrician"],
                    "ineligible_reasons": [],
                    "explanation": "Partial match.",
                },
            ],
        )

        assert match_run.match_run_id
        assert match_run.job_id == "job-electrician"
        assert match_run.options == {"topK": 5, "minimumScore": 0.0}

        results = get_candidate_results(session, match_run.match_run_id)
        assert [result.rank for result in results] == [1, 2]
        assert results[0].employee_id == "emp-alex"
        assert results[0].matched_certifications == ["licensed electrician"]


def test_get_match_run_returns_immutable_stored_run() -> None:
    with _session() as session:
        created = create_match_run(
            session,
            job_id="job-hvac",
            requested_by="supervisor-1",
            model_version="v1",
            snapshot_hash="def456",
            options={},
            results=[],
        )

        fetched = get_match_run(session, created.match_run_id)

        assert fetched is not None
        assert fetched.match_run_id == created.match_run_id
        assert fetched.job_id == "job-hvac"


def test_get_match_run_returns_none_when_missing() -> None:
    with _session() as session:
        assert get_match_run(session, "does-not-exist") is None
