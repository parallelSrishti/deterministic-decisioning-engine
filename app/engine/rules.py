"""Pure deterministic rule engine for application evaluation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.request import ApplicationRequest

RULE_VERSION = "1.0.0"


def evaluate_application(request: ApplicationRequest) -> dict:
    """Evaluate an application and return a deterministic decision.

    Pure function: no randomness, no time-based logic, no external calls,
    no database access, no side effects. Identical input produces identical output.
    """
    base_score = 500

    income_factor = min(request.income_monthly / 20, 200)
    dti_penalty = -100 if request.dti > 0.4 else 0
    employment_factor = min(request.employment_months * 2, 150)
    age_factor = 50 if request.age >= 25 else 0
    defaults_penalty = -300 if request.has_defaults else 0

    score = base_score + income_factor + dti_penalty + employment_factor + age_factor + defaults_penalty
    score = int(score)
    score = max(0, min(score, 1000))

    if score >= 720:
        decision = "APPROVE"
    elif score >= 600:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    reason_codes = []
    if request.income_monthly >= 5000:
        reason_codes.append("HIGH_INCOME")
    if request.dti < 0.3:
        reason_codes.append("LOW_DTI")
    if request.employment_months >= 24:
        reason_codes.append("STABLE_EMPLOYMENT")
    if request.age >= 30:
        reason_codes.append("ESTABLISHED_AGE")
    if not request.has_defaults:
        reason_codes.append("NO_DEFAULTS")
    if request.dti > 0.4:
        reason_codes.append("HIGH_DTI_RISK")
    if request.has_defaults:
        reason_codes.append("HAS_DEFAULTS")

    if decision == "APPROVE":
        explanation = "Application approved based on risk evaluation."
    elif decision == "REVIEW":
        explanation = "Application requires manual review due to moderate risk."
    else:
        explanation = "Application rejected due to high risk factors."

    return {
        "decision": decision,
        "score": score,
        "reason_codes": reason_codes,
        "explanation": explanation,
        "rule_version": RULE_VERSION,
    }
