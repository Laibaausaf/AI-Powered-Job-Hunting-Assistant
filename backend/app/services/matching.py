"""
Deterministic, explainable match-score logic. We deliberately keep the score
itself rule-based (skills overlap) rather than an LLM call - it's fast, free,
reproducible for judging, and easy to explain. The *explanation text* and
skill-gap phrasing can still be LLM-polished in llm_service.py; the score
math lives here so it never changes between calls.
"""
import re
from typing import List, Tuple

# A modest canonical skill vocabulary so we can match "JS" == "JavaScript" etc.
SKILL_ALIASES = {
    "js": "javascript", "ts": "typescript", "py": "python",
    "postgres": "postgresql", "k8s": "kubernetes", "ml": "machine learning",
    "reactjs": "react", "node": "node.js",
}


def _normalize(skill: str) -> str:
    s = skill.strip().lower()
    return SKILL_ALIASES.get(s, s)


def extract_skills_from_text(text: str, vocabulary: List[str]) -> List[str]:
    """Very lightweight keyword-spotting resume/job-description skill extractor.
    `vocabulary` is the list of known skills to look for (e.g. all skills seen
    across seeded jobs). Good enough for a hackathon; swap for an NER model
    or LLM extraction call for the stretch goal."""
    text_l = text.lower()
    found = []
    for skill in vocabulary:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_l):
            found.append(skill)
    return sorted(set(found))


def compute_match(resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str], List[str]]:
    """
    Returns (match_score 0-100, matched_skills, missing_skills).
    Score = overlap / total required job skills, as a percentage.
    """
    if not job_skills:
        return 0.0, [], []

    resume_norm = {_normalize(s) for s in resume_skills}
    job_norm_map = {_normalize(s): s for s in job_skills}  # normalized -> original casing

    matched = [orig for norm, orig in job_norm_map.items() if norm in resume_norm]
    missing = [orig for norm, orig in job_norm_map.items() if norm not in resume_norm]

    score = round(100 * len(matched) / len(job_skills), 1)
    return score, matched, missing


def build_match_explanation(matched: List[str], missing: List[str]) -> str:
    parts = []
    if matched:
        parts.append(f"Matches on: {', '.join(matched)}.")
    if missing:
        parts.append(f"Missing: {', '.join(missing)}.")
    return " ".join(parts) if parts else "No skill data available for this job."
