from collections import Counter
from functools import lru_cache
from re import findall, search

from app.schemas.ats_schema import ATSResponse

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "required",
    "requiring",
    "role",
    "that",
    "the",
    "this",
    "to",
    "with",
    "you",
    "your",
}

TECH_KEYWORDS = {
    "aws",
    "azure",
    "bun",
    "ci/cd",
    "docker",
    "express",
    "fastapi",
    "firebase",
    "gcp",
    "gemini",
    "git",
    "github",
    "hono",
    "javascript",
    "kubernetes",
    "langchain",
    "mongodb",
    "nestjs",
    "next.js",
    "node.js",
    "postgresql",
    "prisma",
    "python",
    "rag",
    "react",
    "redis",
    "rest api",
    "sql",
    "stripe",
    "typescript",
}

ROLE_PATTERNS = (
    r"\bbackend engineer\b",
    r"\bfrontend engineer\b",
    r"\bfull stack engineer\b",
    r"\bfull-stack engineer\b",
    r"\bsoftware engineer\b",
    r"\bai engineer\b",
    r"\bml engineer\b",
    r"\bpython developer\b",
    r"\breact developer\b",
    r"\bnode\.?js developer\b",
)


class ATSScoringService:
    def analyze(self, *, resume_text: str, job_description: str) -> ATSResponse:
        jd_keywords = _extract_keywords(job_description)
        resume_keywords = _extract_keywords(resume_text)

        matched_keywords = sorted(jd_keywords & resume_keywords)
        missing_keywords = sorted(jd_keywords - resume_keywords)

        keyword_score = _percentage(len(matched_keywords), len(jd_keywords))
        role_score = _role_alignment_score(resume_text=resume_text, job_description=job_description)
        coverage_score = _resume_coverage_score(resume_text)
        ats_score = round((keyword_score * 0.6) + (role_score * 0.3) + (coverage_score * 0.1))

        return ATSResponse(
            ats_score=max(0, min(100, ats_score)),
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            suggestions=_build_suggestions(missing_keywords=missing_keywords, role_score=role_score),
        )


def _extract_keywords(text: str) -> set[str]:
    normalized = text.lower()
    words: list[str] = []
    for raw_word in findall(r"[a-z][a-z0-9.+#/-]{1,}", normalized):
        word = raw_word.strip(".-/")
        if word not in STOP_WORDS and len(word) > 2:
            words.append(word)

    tech_matches = {keyword for keyword in TECH_KEYWORDS if keyword in normalized}
    frequent_terms = {
        term
        for term, count in Counter(words).items()
        if count >= 2 and term not in STOP_WORDS
    }

    return set(sorted((tech_matches | frequent_terms | set(words)) - STOP_WORDS)[:50])


def _role_alignment_score(*, resume_text: str, job_description: str) -> int:
    resume = resume_text.lower()
    job = job_description.lower()
    job_roles = {pattern for pattern in ROLE_PATTERNS if search(pattern, job)}

    if not job_roles:
        return 70

    matched_roles = {pattern for pattern in job_roles if search(pattern, resume)}
    if matched_roles:
        return 100

    role_terms = {"backend", "frontend", "full", "stack", "software", "ai", "ml", "python", "react", "node"}
    job_role_terms = {term for term in role_terms if term in job}
    resume_role_terms = {term for term in role_terms if term in resume}

    return _percentage(len(job_role_terms & resume_role_terms), len(job_role_terms))


def _resume_coverage_score(resume_text: str) -> int:
    normalized = resume_text.lower()
    sections = ("summary", "skill", "experience", "project", "education")
    present_sections = sum(1 for section in sections if section in normalized)
    return _percentage(present_sections, len(sections))


def _percentage(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        return 0
    return round((numerator / denominator) * 100)


def _build_suggestions(*, missing_keywords: list[str], role_score: int) -> list[str]:
    suggestions: list[str] = []

    if missing_keywords:
        top_missing = ", ".join(missing_keywords[:8])
        suggestions.append(f"Add truthful evidence for these job keywords where relevant: {top_missing}.")

    if role_score < 70:
        suggestions.append("Align the resume title and summary more closely with the target role.")

    if not suggestions:
        suggestions.append("Keyword coverage and role alignment look strong for this job description.")

    return suggestions


@lru_cache
def get_ats_scoring_service() -> ATSScoringService:
    return ATSScoringService()
