"""Pydantic schema for decision evaluation response."""

from typing import Literal

from pydantic import BaseModel, Field


class DecisionResponse(BaseModel):
    audit_id: str
    decision: Literal["APPROVE", "REVIEW", "REJECT"]
    score: int = Field(ge=0, le=1000)
    reason_codes: list[str]
    explanation: str
    rule_version: str
