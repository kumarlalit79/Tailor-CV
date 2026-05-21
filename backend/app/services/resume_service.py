from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.services.openai_service import OpenAIService, get_openai_service

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "resume_prompt.txt"
MAX_BULLET_WORDS = 50


class ResumeServiceError(Exception):
    """Raised when structured resume generation fails validation."""


class ContactInfo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = None
    role: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None


class ExperienceItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    company: str
    title: str
    start_date: str | None = None
    end_date: str | None = None
    bullets: list[str] = Field(default_factory=list, min_length=1, max_length=4)

    @field_validator("bullets")
    @classmethod
    def validate_bullets(cls, bullets: list[str]) -> list[str]:
        return _validate_bullet_list(bullets)


class ProjectItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    technologies: list[str] = Field(default_factory=list)
    bullets: list[str] = Field(default_factory=list, min_length=1, max_length=3)

    @field_validator("bullets")
    @classmethod
    def validate_bullets(cls, bullets: list[str]) -> list[str]:
        return _validate_bullet_list(bullets)


class EducationItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    institution: str
    degree: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    details: list[str] = Field(default_factory=list, max_length=3)


class StructuredResumeContent(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    contact: ContactInfo = Field(default_factory=ContactInfo)
    summary: str = Field(..., min_length=1, max_length=700)
    technical_skills: list[str] = Field(default_factory=list, min_length=1, max_length=40)
    experience: list[ExperienceItem] = Field(default_factory=list, max_length=4)
    projects: list[ProjectItem] = Field(default_factory=list, max_length=4)
    education: list[EducationItem] = Field(default_factory=list, max_length=3)
    matched_keywords: list[str] = Field(default_factory=list, max_length=50)
    missing_keywords: list[str] = Field(default_factory=list, max_length=30)

    @field_validator("summary")
    @classmethod
    def validate_summary(cls, summary: str) -> str:
        if "—" in summary:
            raise ValueError("summary must not contain em dash characters")
        if len(summary.split()) > 90:
            raise ValueError("summary must stay concise for a single-page resume")
        return summary

    @model_validator(mode="after")
    def validate_no_em_dash(self) -> "StructuredResumeContent":
        if _contains_em_dash(self.model_dump()):
            raise ValueError("resume content must not contain em dash characters")
        return self


class ResumeGenerationService:
    def __init__(self, openai_service: OpenAIService) -> None:
        self.openai_service = openai_service

    async def generate_resume(
        self,
        *,
        resume_text: str,
        job_description: str,
    ) -> dict[str, Any]:
        prompt = _load_resume_prompt()
        system_prompt = _build_system_prompt(prompt)
        user_prompt = _build_user_prompt(resume_text=resume_text, job_description=job_description)

        response = await self.openai_service.create_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format="json",
            max_tokens=3_500,
            temperature=0.2,
        )

        try:
            structured_resume = StructuredResumeContent.model_validate(response)
        except ValueError as exc:
            raise ResumeServiceError("Generated resume did not match the required structure") from exc

        return structured_resume.model_dump()


def _load_resume_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def _build_system_prompt(base_prompt: str) -> str:
    return f"""
{base_prompt}

You are a resume optimization engine for TailorCV.
Return only valid JSON. Do not include Markdown, HTML, CSS, tables, or PDF instructions.
Use only facts present in the provided resume text. Do not invent employers, dates, degrees,
projects, tools, metrics, users, funding, publications, clients, or responsibilities.
If a useful keyword from the job description is not supported by the resume, place it in
missing_keywords instead of adding it to experience or projects.
Never use the em dash character.
Optimize the content for a concise single-page ATS resume.
Keep the summary to 3 lines maximum.
Keep each experience and project bullet under 50 words.

Required JSON shape:
{{
  "contact": {{
    "name": null,
    "role": null,
    "email": null,
    "phone": null,
    "location": null,
    "linkedin": null,
    "github": null,
    "portfolio": null
  }},
  "summary": "string",
  "technical_skills": ["string"],
  "experience": [
    {{
      "company": "string",
      "title": "string",
      "start_date": "string or null",
      "end_date": "string or null",
      "bullets": ["string"]
    }}
  ],
  "projects": [
    {{
      "name": "string",
      "technologies": ["string"],
      "bullets": ["string"]
    }}
  ],
  "education": [
    {{
      "institution": "string",
      "degree": "string or null",
      "start_date": "string or null",
      "end_date": "string or null",
      "details": ["string"]
    }}
  ],
  "matched_keywords": ["string"],
  "missing_keywords": ["string"]
}}
""".strip()


def _build_user_prompt(*, resume_text: str, job_description: str) -> str:
    return f"""
Job Description:
{job_description}

Existing Resume:
{resume_text}

Generate structured ATS-optimized resume content from the existing resume only.
Prioritize the job description keywords when they are truthfully supported by the resume.
""".strip()


def _validate_bullet_list(bullets: list[str]) -> list[str]:
    for bullet in bullets:
        if "—" in bullet:
            raise ValueError("bullet must not contain em dash characters")
        if len(bullet.split()) > MAX_BULLET_WORDS:
            raise ValueError("bullet must be under 50 words")
    return bullets


def _contains_em_dash(value: Any) -> bool:
    if isinstance(value, str):
        return "—" in value
    if isinstance(value, dict):
        return any(_contains_em_dash(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_em_dash(item) for item in value)
    return False


def flatten_resume_content(resume_data: Mapping[str, Any]) -> str:
    parts: list[str] = []

    contact = resume_data.get("contact") or {}
    if isinstance(contact, Mapping):
        parts.extend(str(value) for value in contact.values() if value)

    for key in ("summary", "technical_skills", "experience", "projects", "education"):
        value = resume_data.get(key)
        _append_plain_text(parts, value)

    return "\n".join(parts)


def _append_plain_text(parts: list[str], value: Any) -> None:
    if isinstance(value, str):
        parts.append(value)
    elif isinstance(value, Mapping):
        for item in value.values():
            _append_plain_text(parts, item)
    elif isinstance(value, list):
        for item in value:
            _append_plain_text(parts, item)


@lru_cache
def get_resume_generation_service() -> ResumeGenerationService:
    return ResumeGenerationService(openai_service=get_openai_service())
