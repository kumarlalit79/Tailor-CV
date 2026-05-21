from functools import lru_cache
from pathlib import Path
from typing import Any

from app.schemas.cover_letter_schema import CoverLetterResponse
from app.services.openai_service import OpenAIService, get_openai_service

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "cover_letter_prompt.txt"


class CoverLetterServiceError(Exception):
    """Raised when cover letter generation fails validation."""


class CoverLetterService:
    def __init__(self, openai_service: OpenAIService) -> None:
        self.openai_service = openai_service

    async def generate_cover_letter(
        self,
        *,
        optimized_resume: str,
        job_description: str,
    ) -> CoverLetterResponse:
        response = await self.openai_service.create_completion(
            system_prompt=_build_system_prompt(_load_cover_letter_prompt()),
            user_prompt=_build_user_prompt(
                optimized_resume=optimized_resume,
                job_description=job_description,
            ),
            response_format="json",
            max_tokens=1_200,
            temperature=0.3,
        )

        try:
            return CoverLetterResponse.model_validate(_normalize_response(response))
        except ValueError as exc:
            raise CoverLetterServiceError(
                "Generated cover letter did not match the required structure"
            ) from exc


def _load_cover_letter_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def _build_system_prompt(base_prompt: str) -> str:
    return f"""
{base_prompt}

Generate only a concise professional cover letter.
Return only valid JSON. Do not include Markdown, HTML, bullets, or extra commentary.
Never use the em dash character.
Keep the tone professional, specific to the job description, and truthful to the resume.
Do not invent experience, metrics, companies, links, education, tools, or availability.

Required JSON shape:
{{
  "cover_letter": "string"
}}
""".strip()


def _build_user_prompt(*, optimized_resume: str, job_description: str) -> str:
    return f"""
Job Description:
{job_description}

Optimized Resume:
{optimized_resume}

Write a cover letter based only on the resume and job description.
""".strip()


def _normalize_response(response: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(response, dict):
        return response
    return {"cover_letter": response}


@lru_cache
def get_cover_letter_service() -> CoverLetterService:
    return CoverLetterService(openai_service=get_openai_service())
