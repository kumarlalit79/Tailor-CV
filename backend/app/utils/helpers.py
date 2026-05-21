from re import sub
from typing import Any


def sanitize_text_input(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("value must be a string")

    sanitized = value.replace("\x00", "")
    sanitized = sub(r"(?is)<(script|style).*?>.*?</\1>", " ", sanitized)
    sanitized = sub(r"(?s)<[^>]*>", " ", sanitized)
    sanitized = sub(r"[ \t\r\f\v]+", " ", sanitized)
    sanitized = sub(r"\n{3,}", "\n\n", sanitized)

    return sanitized.strip()


def contains_em_dash(value: str) -> bool:
    return "—" in value


def count_words(value: str) -> int:
    return len(value.split())
