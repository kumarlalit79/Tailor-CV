from functools import lru_cache
import logging
from pathlib import Path
from typing import Any, Mapping

from jinja2 import Environment, FileSystemLoader, select_autoescape

APP_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
RESUME_TEMPLATE = "resume_template.html"
RESUME_CSS = "resume.css"
logger = logging.getLogger(__name__)


class ResumeRenderService:
    def __init__(self) -> None:
        logger.debug("Initializing resume renderer. templates_dir=%s", TEMPLATES_DIR)
        self.environment = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(("html", "xml")),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_resume(self, resume_data: Mapping[str, Any]) -> str:
        logger.debug("Loading resume template. template=%s", RESUME_TEMPLATE)
        try:
            template = self.environment.get_template(RESUME_TEMPLATE)
        except Exception as exc:
            logger.exception(
                "Resume template loading failed. template=%s templates_dir=%s exception_type=%s",
                RESUME_TEMPLATE,
                TEMPLATES_DIR,
                type(exc).__name__,
            )
            raise
        logger.debug("Resume template loaded successfully. template=%s", RESUME_TEMPLATE)

        css = _load_resume_css()
        logger.debug("Resume CSS loaded successfully. css_file=%s css_length=%s", RESUME_CSS, len(css))

        html = template.render(
            resume=_normalize_resume_data(resume_data),
            resume_css=css,
        )
        logger.info(
            "Resume HTML rendered successfully. html_length=%s has_contact=%s",
            len(html),
            bool((resume_data.get("contact") or {}).get("name"))
            if isinstance(resume_data.get("contact"), Mapping)
            else False,
        )
        return html


def _normalize_resume_data(resume_data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contact": resume_data.get("contact") or {},
        "summary": resume_data.get("summary") or "",
        "technical_skills": _normalize_technical_skills(resume_data.get("technical_skills")),
        "experience": resume_data.get("experience") or [],
        "projects": resume_data.get("projects") or [],
        "education": resume_data.get("education") or [],
    }


def _normalize_technical_skills(value: Any) -> dict[str, list[str]]:
    empty_groups = {
        "frontend": [],
        "backend": [],
        "databases": [],
        "tools_devops": [],
        "familiar_with": [],
    }

    if isinstance(value, Mapping):
        return {
            key: _normalize_string_list(value.get(key))
            for key in empty_groups
        }

    if isinstance(value, list):
        return {**empty_groups, "familiar_with": _normalize_string_list(value)}

    return empty_groups


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    return [str(item) for item in value if item]


def _load_resume_css() -> str:
    css_path = STATIC_DIR / RESUME_CSS
    try:
        return css_path.read_text(encoding="utf-8")
    except Exception as exc:
        logger.exception(
            "Resume CSS loading failed. css_path=%s exception_type=%s",
            css_path,
            type(exc).__name__,
        )
        raise


@lru_cache
def get_resume_render_service() -> ResumeRenderService:
    return ResumeRenderService()
