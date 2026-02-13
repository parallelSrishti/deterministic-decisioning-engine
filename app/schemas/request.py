"""Pydantic schema for application submission input."""

from pydantic import BaseModel, Field


class ApplicationRequest(BaseModel):
    income_monthly: int = Field(ge=0, description="Monthly income")
    dti: float = Field(ge=0.0, le=5.0, description="Debt-to-income ratio")
    employment_months: int = Field(ge=0, description="Employment duration in months")
    age: int = Field(ge=18, description="Applicant age")
    has_defaults: bool = Field(description="Has payment defaults")
