"""Pure eligibility evaluation from dated credential evidence at a fixed snapshot."""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field

from skillmatch.features.matching.canonical_scoring import JobScoringInput


class _FrozenModel(BaseModel):
    model_config = {'frozen': True, 'extra': 'forbid'}


class CertificationEvidence(_FrozenModel):
    code: Annotated[str, Field(min_length=1)]
    issued_on: date
    expires_on: date | None = None


class EmployeeEligibilityInput(_FrozenModel):
    status: str
    certifications: tuple[CertificationEvidence, ...]


class EligibilityResult(_FrozenModel):
    eligible: bool
    valid_certification_codes: frozenset[str]
    matched_certifications: tuple[str, ...]
    missing_certifications: tuple[str, ...]
    ineligible_reasons: tuple[str, ...]


def evaluate_eligibility(
    employee: EmployeeEligibilityInput, job: JobScoringInput, *, as_of: date,
) -> EligibilityResult:
    """Return eligibility and evidence without inspecting skills or the current clock.

    A credential is valid from its issue date through its expiration date,
    inclusive. Any currently valid renewal satisfies its code even if an older
    record has expired. Reasons and required-credential evidence have stable
    ordering independent of input ordering.
    """
    valid_codes = frozenset(
        credential.code for credential in employee.certifications
        if credential.issued_on <= as_of
        and (credential.expires_on is None or credential.expires_on >= as_of)
    )
    missing = tuple(sorted(job.required_certification_codes - valid_codes))
    matched = tuple(sorted(job.required_certification_codes & valid_codes))
    reasons = (() if employee.status == 'ACTIVE' else ('EMPLOYEE_NOT_ACTIVE',)) + tuple(
        f'MISSING_MANDATORY_CERTIFICATION:{code}' for code in missing
    )
    return EligibilityResult(
        eligible=not reasons, valid_certification_codes=valid_codes,
        matched_certifications=matched, missing_certifications=missing,
        ineligible_reasons=reasons,
    )
