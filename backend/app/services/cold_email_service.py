from functools import lru_cache
from pathlib import Path
from typing import Any

from app.schemas.cold_email_schema import ColdEmailResponse
from app.services.openai_service import OpenAIService, get_openai_service

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "cold_email_prompt.txt"


class ColdEmailServiceError(Exception):
    """Raised when cold email generation fails validation."""


class ColdEmailService:
    def __init__(self, openai_service: OpenAIService) -> None:
        self.openai_service = openai_service

    async def generate_cold_email(
        self,
        *,
        optimized_resume: str,
        job_description: str,
    ) -> ColdEmailResponse:
        response = await self.openai_service.create_completion(
            system_prompt=_build_system_prompt(_load_cold_email_prompt()),
            user_prompt=_build_user_prompt(
                optimized_resume=optimized_resume,
                job_description=job_description,
            ),
            response_format="json",
            max_tokens=900,
            temperature=0.35,
        )

        try:
            return ColdEmailResponse.model_validate(_normalize_response(response))
        except ValueError as exc:
            raise ColdEmailServiceError(
                "Generated cold email did not match the required structure"
            ) from exc


def _load_cold_email_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def _build_system_prompt(base_prompt: str) -> str:
    return f"""
{base_prompt}

Generate only one concise cold email for a founder, recruiter, or hiring manager.
Return only valid JSON. Do not include Markdown, HTML, bullets, or extra commentary.
The cold email must be 100 to 150 words.
Use a confident, warm, founder/recruiter-friendly tone.
Never use the em dash character.
Do not invent experience, metrics, companies, links, education, tools, or availability.
Do not add portfolio or GitHub links.

Required JSON shape:
{{
  "cold_email": "string"
}}
""".strip()


def _build_user_prompt(*, optimized_resume: str, job_description: str) -> str:
    return f"""
Job Description:
{job_description}

Optimized Resume:
{optimized_resume}

Write a personalized cold email based only on the resume and job description.
""".strip()


def _normalize_response(response: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(response, dict):
        return response
    return {"cold_email": response}


@lru_cache
def get_cold_email_service() -> ColdEmailService:
    return ColdEmailService(openai_service=get_openai_service())
