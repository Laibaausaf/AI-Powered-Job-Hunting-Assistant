"""
All calls to the Claude API live in this file. Centralizing them makes it
easy to (a) swap models, (b) add response caching to stay under rate limits
during judging (Section 9), and (c) keep prompts consistent.

Every function asks Claude to return ONLY JSON so we can parse it directly -
see the `_extract_json` helper for defensive parsing (models occasionally
wrap JSON in prose or code fences despite instructions).
"""
import json
import re
from typing import List, Dict, Any, Optional

from anthropic import Anthropic

from app.config import settings

_client: Optional[Anthropic] = None


def get_client() -> Anthropic:
    global _client
    if _client is None:
        if not settings.ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _client


def _call(system: str, user: str, max_tokens: int = 1200) -> str:
    client = get_client()
    resp = client.messages.create(
        model=settings.CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def _extract_json(text: str) -> Any:
    """Strip markdown code fences if present, then parse JSON. Raises with
    the raw text included so failures are debuggable during judging demos."""
    cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM did not return valid JSON: {e}\nRaw output:\n{text}")


# ---------- Module B: tailoring ----------
def generate_bullets_and_letter(
    resume_text: str, job_description: str, matched_skills: List[str],
    missing_skills: List[str], job_title: str, company: str,
) -> Dict[str, Any]:
    system = (
        "You are a career coach helping a candidate tailor their application. "
        "Respond with ONLY a JSON object, no prose, no markdown fences."
    )
    user = f"""
Resume:
---
{resume_text[:4000]}
---

Job description ({job_title} at {company}):
---
{job_description[:3000]}
---

Skills the candidate already has that match this job: {matched_skills}
Skills required by the job but missing from the resume: {missing_skills}

Return a JSON object with exactly these keys:
- "resume_bullet_suggestions": a list of at least 5 specific, tailored resume
  bullet points the candidate could add or rewrite to better match this job.
  Each bullet should reference a real skill/gap from above, phrased as an
  achievement (action verb + what + measurable impact where plausible).
- "cover_letter": a 250-400 word cover letter draft. It MUST explicitly
  mention the job title "{job_title}", the company "{company}", and at least
  2-3 concrete matched qualifications from the resume. Do not use generic
  boilerplate like "I am writing to express my interest" without specifics.
"""
    data = _extract_json(_call(system, user))
    data.setdefault("resume_bullet_suggestions", [])
    data.setdefault("cover_letter", "")
    return data


def extract_autofill_fields(resume_text: str) -> Dict[str, Any]:
    system = "Extract structured contact/profile info. Respond with ONLY JSON."
    user = f"""
Resume text:
---
{resume_text[:4000]}
---
Return a JSON object with exactly these keys: "name", "email",
"experience_summary" (1-2 sentence summary of their experience), and
"skills" (list of strings). Use null for any field you cannot find.
"""
    return _extract_json(_call(system, user, max_tokens=600))


# ---------- Module C: interview prep ----------
def generate_interview_questions(job_description: str, num_questions: int = 8) -> List[Dict[str, Any]]:
    system = (
        "You are an interview coach. Respond with ONLY a JSON array, no prose."
    )
    user = f"""
Job description:
---
{job_description[:3000]}
---

Generate exactly {num_questions} interview questions for this role, split
across three categories: "behavioral", "technical", and "culture_fit".
Include at least 2 of each category. Questions must be specific to details
in the job description above (technologies, responsibilities mentioned),
not generic.

Return a JSON array where each item has exactly these keys:
- "category": one of "behavioral", "technical", "culture_fit"
- "question": the interview question text
- "answer_outline": a list of 3-5 short bullet points describing what a
  strong answer should cover. For "behavioral" questions, structure this
  around the STAR method (Situation, Task, Action, Result).
"""
    return _extract_json(_call(system, user, max_tokens=1800))


def evaluate_answer(question: str, answer_text: str, answer_outline: List[str]) -> Dict[str, Any]:
    system = "You are an interview coach giving constructive feedback. Respond with ONLY JSON."
    user = f"""
Interview question: {question}
What a strong answer should cover: {answer_outline}

Candidate's answer:
---
{answer_text[:2000]}
---

Return a JSON object with exactly these keys:
- "clarity": integer 1-5
- "structure": integer 1-5
- "relevance": integer 1-5
- "notes": 2-3 sentences of specific, constructive feedback referencing what
  the candidate said and what they could improve, in an encouraging tone.
"""
    return _extract_json(_call(system, user, max_tokens=500))
