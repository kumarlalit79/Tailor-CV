from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from jinja2 import Environment, FileSystemLoader, select_autoescape

APP_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
RESUME_TEMPLATE = "resume_template.html"
RESUME_CSS = "resume.css"


class ResumeRenderService:
    def __init__(self) -> None:
        self.environment = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(("html", "xml")),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_resume(self, resume_data: Mapping[str, Any]) -> str:
        template = self.environment.get_template(RESUME_TEMPLATE)
        return template.render(
            resume=_normalize_resume_data(resume_data),
            resume_css=_load_resume_css(),
        )


def _normalize_resume_data(resume_data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contact": resume_data.get("contact") or {},
        "summary": resume_data.get("summary") or "",
        "technical_skills": resume_data.get("technical_skills") or [],
        "experience": resume_data.get("experience") or [],
        "projects": resume_data.get("projects") or [],
        "education": resume_data.get("education") or [],
    }


def _load_resume_css() -> str:
    return (STATIC_DIR / RESUME_CSS).read_text(encoding="utf-8")


@lru_cache
def get_resume_render_service() -> ResumeRenderService:
    return ResumeRenderService()
