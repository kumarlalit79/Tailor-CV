from functools import lru_cache
from re import search

from app.services.ats_service import extract_ats_keywords, extract_technical_skills

ROLE_PATTERNS = (
    "backend engineer",
    "frontend engineer",
    "full stack engineer",
    "full-stack engineer",
    "software engineer",
    "ai engineer",
    "ml engineer",
    "python developer",
    "react developer",
    "node.js developer",
)


class JDAnalysisService:
    def analyze(self, *, job_description: str) -> dict[str, list[str] | str | None]:
        normalized = job_description.lower()
        skills = extract_technical_skills(job_description)
        keywords = extract_ats_keywords(job_description)

        return {
            "role": _extract_role(normalized),
            "skills": skills,
            "keywords": keywords,
        }


def _extract_role(normalized_job_description: str) -> str | None:
    for role in ROLE_PATTERNS:
        if role in normalized_job_description:
            return role.title().replace("Ai", "AI").replace("Ml", "ML")

    title_match = search(
        r"\b([a-z]+(?:\s+[a-z]+){0,3}\s+(?:engineer|developer))\b",
        normalized_job_description,
    )
    return title_match.group(1).title() if title_match else None


@lru_cache
def get_jd_analysis_service() -> JDAnalysisService:
    return JDAnalysisService()
