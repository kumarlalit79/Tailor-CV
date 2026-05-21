from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators import (
    MAX_JOB_DESCRIPTION_LENGTH,
    MAX_RESUME_LENGTH,
    MIN_JOB_DESCRIPTION_LENGTH,
    MIN_RESUME_LENGTH,
    validate_job_description,
    validate_resume_text,
)


class ResumeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    job_description: str = Field(
        ..., min_length=MIN_JOB_DESCRIPTION_LENGTH, max_length=MAX_JOB_DESCRIPTION_LENGTH
    )
    resume_text: str = Field(..., min_length=MIN_RESUME_LENGTH, max_length=MAX_RESUME_LENGTH)

    @field_validator("job_description", mode="before")
    @classmethod
    def sanitize_job_description(cls, value: str) -> str:
        return validate_job_description(value)

    @field_validator("resume_text", mode="before")
    @classmethod
    def sanitize_resume_text(cls, value: str) -> str:
        return validate_resume_text(value)


class ResumeResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    optimized_resume: dict[str, Any] = Field(default_factory=dict)
    ats_score: int = Field(..., ge=0, le=100)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    pdf_url: str | None = None
    file_name: str | None = None

    @field_validator("optimized_resume")
    @classmethod
    def validate_ats_safe_content(cls, value: dict[str, Any]) -> dict[str, Any]:
        if _contains_em_dash(value):
            raise ValueError("optimized_resume must not contain em dash characters")
        return value


def _contains_em_dash(value: Any) -> bool:
    if isinstance(value, str):
        return "—" in value
    if isinstance(value, dict):
        return any(_contains_em_dash(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_em_dash(item) for item in value)
    return False
