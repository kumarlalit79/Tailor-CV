from app.utils.helpers import contains_em_dash, count_words, sanitize_text_input

MIN_RESUME_LENGTH = 50
MAX_RESUME_LENGTH = 20_000
MIN_JOB_DESCRIPTION_LENGTH = 50
MAX_JOB_DESCRIPTION_LENGTH = 20_000
MIN_GENERATED_LENGTH = 1
MAX_GENERATED_LENGTH = 20_000


def validate_resume_text(value: str) -> str:
    return validate_text_length(
        value,
        field_name="resume_text",
        min_length=MIN_RESUME_LENGTH,
        max_length=MAX_RESUME_LENGTH,
    )


def validate_job_description(value: str) -> str:
    return validate_text_length(
        value,
        field_name="job_description",
        min_length=MIN_JOB_DESCRIPTION_LENGTH,
        max_length=MAX_JOB_DESCRIPTION_LENGTH,
    )


def validate_generated_text(
    value: str,
    *,
    field_name: str,
    max_length: int = MAX_GENERATED_LENGTH,
    allow_em_dash: bool = False,
) -> str:
    sanitized = validate_text_length(
        value,
        field_name=field_name,
        min_length=MIN_GENERATED_LENGTH,
        max_length=max_length,
    )

    if not allow_em_dash and contains_em_dash(sanitized):
        raise ValueError(f"{field_name} must not contain em dash characters")

    return sanitized


def validate_word_count(value: str, *, field_name: str, min_words: int, max_words: int) -> str:
    word_count = count_words(value)

    if not min_words <= word_count <= max_words:
        raise ValueError(f"{field_name} must be between {min_words} and {max_words} words")

    return value


def validate_text_length(
    value: str,
    *,
    field_name: str,
    min_length: int,
    max_length: int,
) -> str:
    sanitized = sanitize_text_input(value)
    text_length = len(sanitized)

    if text_length < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters")

    if text_length > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters")

    return sanitized
