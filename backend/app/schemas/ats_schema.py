from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators import (
    MAX_JOB_DESCRIPTION_LENGTH,
    MAX_RESUME_LENGTH,
    MIN_JOB_DESCRIPTION_LENGTH,
    MIN_RESUME_LENGTH,
    validate_job_description,
    validate_resume_text,
)


class ATSRequest(BaseModel):
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


class ATSResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    ats_score: int = Field(..., ge=0, le=100)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
