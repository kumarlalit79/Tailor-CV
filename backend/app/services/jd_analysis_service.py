from functools import lru_cache
from re import findall, search

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

SKILL_KEYWORDS = {
    "aws",
    "azure",
    "docker",
    "fastapi",
    "firebase",
    "gcp",
    "javascript",
    "kubernetes",
    "mongodb",
    "nestjs",
    "next.js",
    "node.js",
    "postgresql",
    "prisma",
    "python",
    "react",
    "redis",
    "rest api",
    "sql",
    "typescript",
}

STOP_WORDS = {
    "and",
    "are",
    "for",
    "from",
    "our",
    "the",
    "this",
    "with",
    "you",
    "your",
}


class JDAnalysisService:
    def analyze(self, *, job_description: str) -> dict[str, list[str] | str | None]:
        normalized = job_description.lower()
        skills = sorted(skill for skill in SKILL_KEYWORDS if skill in normalized)
        keywords = _extract_keywords(normalized, skills)

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


def _extract_keywords(normalized_job_description: str, skills: list[str]) -> list[str]:
    words = {
        word.strip(".-/")
        for word in findall(r"[a-z][a-z0-9.+#/-]{2,}", normalized_job_description)
    }
    keywords = {word for word in words if word and word not in STOP_WORDS}

    return sorted((keywords | set(skills)))[:50]


@lru_cache
def get_jd_analysis_service() -> JDAnalysisService:
    return JDAnalysisService()
