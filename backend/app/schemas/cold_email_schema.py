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
    validate_word_count,
)

COLD_EMAIL_MAX_LENGTH = 2_500
COLD_EMAIL_MIN_WORDS = 100
COLD_EMAIL_MAX_WORDS = 150


class ColdEmailRequest(BaseModel):
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


class ColdEmailResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cold_email: str = Field(..., min_length=MIN_GENERATED_LENGTH, max_length=COLD_EMAIL_MAX_LENGTH)

    @field_validator("cold_email")
    @classmethod
    def validate_cold_email_constraints(cls, value: str) -> str:
        validated = validate_generated_text(
            value,
            field_name="cold_email",
            max_length=COLD_EMAIL_MAX_LENGTH,
        )
        return validate_word_count(
            validated,
            field_name="cold_email",
            min_words=COLD_EMAIL_MIN_WORDS,
            max_words=COLD_EMAIL_MAX_WORDS,
        )
