from collections import Counter
from functools import lru_cache
from re import escape, findall, search, sub

from app.schemas.ats_schema import ATSResponse

STOP_WORDS = {
    "a",
    "able",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "about",
    "across",
    "also",
    "apply",
    "around",
    "be",
    "best",
    "both",
    "by",
    "can",
    "company",
    "communication",
    "each",
    "etc",
    "for",
    "follow",
    "from",
    "good",
    "great",
    "have",
    "help",
    "in",
    "into",
    "is",
    "it",
    "its",
    "more",
    "most",
    "not",
    "of",
    "on",
    "or",
    "our",
    "own",
    "required",
    "requiring",
    "role",
    "should",
    "such",
    "that",
    "the",
    "their",
    "they",
    "this",
    "through",
    "to",
    "using",
    "will",
    "with",
    "work",
    "working",
    "you",
    "your",
}

LOW_VALUE_RESUME_WORDS = {
    "advanced",
    "ability",
    "basic",
    "build",
    "built",
    "create",
    "created",
    "creating",
    "develop",
    "developed",
    "developing",
    "excellent",
    "experience",
    "familiar",
    "fast",
    "hands",
    "high",
    "highly",
    "implement",
    "implemented",
    "improve",
    "improved",
    "knowledge",
    "learn",
    "learning",
    "manage",
    "managed",
    "nice",
    "passionate",
    "proficient",
    "responsible",
    "scalable",
    "simple",
    "solid",
    "strong",
    "team",
    "user",
}

GENERIC_FILTER_WORDS = STOP_WORDS | LOW_VALUE_RESUME_WORDS

TECH_KEYWORDS: dict[str, tuple[str, ...]] = {
    "ASP.NET": ("asp.net", "asp net"),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure", "microsoft azure"),
    "Bun": ("bun",),
    "C#": ("c#", "c sharp"),
    "C++": ("c++",),
    "CI/CD": ("ci/cd", "ci cd", "continuous integration", "continuous delivery"),
    "CSS": ("css",),
    "Django": ("django",),
    "Docker": ("docker",),
    "Express": ("express", "express.js", "expressjs"),
    "FastAPI": ("fastapi", "fast api"),
    "Firebase": ("firebase",),
    "Flask": ("flask",),
    "GCP": ("gcp", "google cloud"),
    "Gemini": ("gemini",),
    "Git": ("git",),
    "GitHub": ("github",),
    "GraphQL": ("graphql", "graph ql"),
    "HTML": ("html",),
    "Hono": ("hono",),
    "Java": ("java",),
    "JavaScript": ("javascript", "java script"),
    "JWT": ("jwt", "json web token", "json web tokens"),
    "Kubernetes": ("kubernetes", "k8s"),
    "LangChain": ("langchain", "lang chain"),
    "MongoDB": ("mongodb", "mongo db"),
    "MySQL": ("mysql", "my sql"),
    "NestJS": ("nestjs", "nest.js", "nest js"),
    "Next.js": ("next.js", "nextjs", "next js"),
    "Node.js": ("node.js", "nodejs", "node js"),
    "PostgreSQL": ("postgresql", "postgres", "postgre sql"),
    "Prisma": ("prisma",),
    "Python": ("python",),
    "RAG": ("rag", "retrieval augmented generation"),
    "React": ("react", "react.js", "reactjs"),
    "Redis": ("redis",),
    "REST APIs": ("rest api", "rest apis", "restful api", "restful apis"),
    "SQL": ("sql",),
    "Stripe": ("stripe",),
    "Tailwind CSS": ("tailwind css", "tailwind"),
    "TypeScript": ("typescript", "type script"),
    "Vercel": ("vercel",),
}

ROLE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "API development": ("api development",),
    "Backend": ("backend", "back end"),
    "Data structures": ("data structures",),
    "Distributed systems": ("distributed systems",),
    "Frontend": ("frontend", "front end"),
    "Full stack": ("full stack", "full-stack"),
    "Machine learning": ("machine learning",),
    "Microservices": ("microservices", "micro services"),
    "Object-oriented programming": (
        "object-oriented programming",
        "object oriented programming",
        "oop",
    ),
    "System design": ("system design",),
    "Unit testing": ("unit testing", "unit tests"),
}

KNOWN_TERM_ALIASES = {
    alias
    for aliases in (*TECH_KEYWORDS.values(), *ROLE_KEYWORDS.values())
    for alias in aliases
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
    r"\bnode(?:\s+)?js developer\b",
)


class ATSScoringService:
    def analyze(self, *, resume_text: str, job_description: str) -> ATSResponse:
        jd_keywords = _extract_keywords(job_description)
        resume_keywords = _extract_keywords(resume_text)

        matched_keywords = sorted(jd_keywords & resume_keywords)
        missing_keywords = _resolve_missing_keyword_conflicts(
            missing_keywords=jd_keywords - resume_keywords,
            matched_keywords=set(matched_keywords),
        )

        keyword_score = _weighted_keyword_score(
            jd_keywords=jd_keywords,
            matched_keywords=set(matched_keywords),
        )
        role_score = _role_alignment_score(resume_text=resume_text, job_description=job_description)
        coverage_score = _resume_coverage_score(resume_text)
        ats_score = round((keyword_score * 0.7) + (role_score * 0.25) + (coverage_score * 0.05))

        return ATSResponse(
            ats_score=max(0, min(100, ats_score)),
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            suggestions=_build_suggestions(missing_keywords=missing_keywords, role_score=role_score),
        )


def _extract_keywords(text: str) -> set[str]:
    normalized = _normalize_text(text)
    tech_matches = _match_known_terms(normalized, TECH_KEYWORDS)
    role_matches = _match_known_terms(normalized, ROLE_KEYWORDS)

    phrase_matches = {
        phrase
        for phrase in _extract_technical_phrases(normalized)
        if not _contains_known_term_alias(phrase)
    }
    repeated_role_terms = _extract_repeated_role_terms(normalized)

    keywords = tech_matches | role_matches | phrase_matches | repeated_role_terms
    return set(sorted(keywords, key=str.lower)[:50])


def extract_ats_keywords(text: str) -> list[str]:
    return sorted(_extract_keywords(text), key=str.lower)


def extract_technical_skills(text: str) -> list[str]:
    return sorted(_match_known_terms(_normalize_text(text), TECH_KEYWORDS), key=str.lower)


def _match_known_terms(normalized_text: str, terms: dict[str, tuple[str, ...]]) -> set[str]:
    matches: set[str] = set()
    for canonical, aliases in terms.items():
        for alias in aliases:
            pattern = rf"(?<![a-z0-9]){escape(_normalize_text(alias))}(?![a-z0-9])"
            if search(pattern, normalized_text):
                matches.add(canonical)
                break
    return matches


def _normalize_text(text: str) -> str:
    normalized = text.lower()
    normalized = normalized.replace("&", " and ")
    normalized = sub(r"(?<=[a-z0-9])/(?=[a-z0-9])", " ", normalized)
    normalized = sub(r"(?<=[a-z])\.(?=[a-z])", " ", normalized)
    normalized = sub(r"(?<=[a-z0-9])-(?=[a-z0-9])", " ", normalized)
    normalized = sub(r"[^a-z0-9+#\s]", " ", normalized)
    return sub(r"\s+", " ", normalized).strip()


def _contains_known_term_alias(phrase: str) -> bool:
    normalized_phrase = _normalize_text(phrase)
    return any(
        search(rf"(?<![a-z0-9]){escape(_normalize_text(alias))}(?![a-z0-9])", normalized_phrase)
        for alias in KNOWN_TERM_ALIASES
    )


def _resolve_missing_keyword_conflicts(
    *,
    missing_keywords: set[str],
    matched_keywords: set[str],
) -> list[str]:
    normalized_matches = {_normalize_text(keyword) for keyword in matched_keywords}
    filtered_missing: set[str] = set()

    for keyword in missing_keywords:
        normalized_keyword = _normalize_text(keyword)
        if normalized_keyword in normalized_matches:
            continue

        if any(
            search(rf"(?<![a-z0-9]){escape(match)}(?![a-z0-9])", normalized_keyword)
            for match in normalized_matches
        ):
            continue

        filtered_missing.add(keyword)

    return sorted(filtered_missing, key=str.lower)


def _extract_technical_phrases(normalized_text: str) -> set[str]:
    phrases: set[str] = set()
    for raw_phrase in findall(
        r"\b[a-z][a-z0-9+#]*(?:\s+[a-z][a-z0-9+#]*){1,3}\b",
        normalized_text,
    ):
        phrase = " ".join(
            word.strip(".-/")
            for word in raw_phrase.split()
            if word.strip(".-/") and word.strip(".-/") not in GENERIC_FILTER_WORDS
        )
        if _is_meaningful_technical_phrase(phrase):
            phrases.add(phrase)
    return phrases


def _extract_repeated_role_terms(normalized_text: str) -> set[str]:
    words = [
        raw_word.strip(".-/")
        for raw_word in findall(r"[a-z][a-z0-9.+#/-]{2,}", normalized_text)
    ]
    role_terms = {
        "authentication",
        "automation",
        "deployment",
        "infrastructure",
        "integration",
        "observability",
        "optimization",
        "performance",
        "scalability",
        "security",
        "testing",
    }
    return {
        term
        for term, count in Counter(words).items()
        if count >= 2 and term in role_terms and term not in GENERIC_FILTER_WORDS
    }


def _is_meaningful_technical_phrase(phrase: str) -> bool:
    if not phrase or phrase in GENERIC_FILTER_WORDS:
        return False

    words = phrase.split()
    if not (2 <= len(words) <= 4):
        return False

    if any(word in GENERIC_FILTER_WORDS for word in words):
        return False

    technical_markers = {
        "api",
        "apis",
        "architecture",
        "auth",
        "authentication",
        "cloud",
        "database",
        "databases",
        "deployment",
        "developer",
        "engineering",
        "framework",
        "infrastructure",
        "integration",
        "microservice",
        "microservices",
        "pipeline",
        "pipelines",
        "platform",
        "security",
        "services",
        "stack",
        "systems",
        "testing",
        "tools",
    }
    return any(marker in words for marker in technical_markers)


def _weighted_keyword_score(*, jd_keywords: set[str], matched_keywords: set[str]) -> int:
    if not jd_keywords:
        return 0

    def weight(keyword: str) -> float:
        if keyword in TECH_KEYWORDS:
            return 2.5
        if keyword in ROLE_KEYWORDS:
            return 1.25
        return 1.0

    total_weight = sum(weight(keyword) for keyword in jd_keywords)
    matched_weight = sum(weight(keyword) for keyword in matched_keywords)
    return round((matched_weight / total_weight) * 100)


def _role_alignment_score(*, resume_text: str, job_description: str) -> int:
    resume = _normalize_text(resume_text)
    job = _normalize_text(job_description)
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
