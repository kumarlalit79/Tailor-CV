from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators import (
    MAX_JOB_DESCRIPTION_LENGTH,
    MAX_RESUME_LENGTH,
    MIN_GENERATED_LENGTH,
    MIN_JOB_DESCRIPTION_LENGTH,
    MIN_RESUME_LENGTH,
    validate_generated_text,
    validate_job_description,
    validate_resume_text,
)

COVER_LETTER_MAX_LENGTH = 5_000


class CoverLetterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    optimized_resume: str = Field(..., min_length=MIN_RESUME_LENGTH, max_length=MAX_RESUME_LENGTH)
    job_description: str = Field(
        ..., min_length=MIN_JOB_DESCRIPTION_LENGTH, max_length=MAX_JOB_DESCRIPTION_LENGTH
    )

    @field_validator("optimized_resume", mode="before")
    @classmethod
    def sanitize_optimized_resume(cls, value: str) -> str:
        return validate_resume_text(value)

    @field_validator("job_description", mode="before")
    @classmethod
    def sanitize_job_description(cls, value: str) -> str:
        return validate_job_description(value)


class CoverLetterResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cover_letter: str = Field(
        ..., min_length=MIN_GENERATED_LENGTH, max_length=COVER_LETTER_MAX_LENGTH
    )

    @field_validator("cover_letter")
    @classmethod
    def validate_no_em_dash(cls, value: str) -> str:
        return validate_generated_text(
            value,
            field_name="cover_letter",
            max_length=COVER_LETTER_MAX_LENGTH,
        )
