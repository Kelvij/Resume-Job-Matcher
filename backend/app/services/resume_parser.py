import re
from .normalize import SKILL_GROUPS, normalize_skills
from .text_utils import clean_text, contains_term, split_sentences

SECTION_NAMES = [
    "skills", "technical skills", "experience", "work experience", "projects", "education",
    "certifications", "achievements", "summary", "profile"
]


def _extract_skills(text: str) -> list[str]:
    found: list[str] = []
    for canonical, aliases in SKILL_GROUPS.items():
        if any(contains_term(text, alias) for alias in aliases):
            found.append(canonical)
    return normalize_skills(found)


def _sections(text: str) -> dict[str, str]:
    lines = [line.strip() for line in text.replace("•", "\n").splitlines() if line.strip()]
    if len(lines) <= 4:
        lines = split_sentences(text)
    result: dict[str, list[str]] = {name: [] for name in SECTION_NAMES}
    current = "summary"
    for line in lines:
        key = line.lower().strip(" :")
        if key in SECTION_NAMES:
            current = key
            continue
        result.setdefault(current, []).append(line)
    return {k: clean_text(" ".join(v)) for k, v in result.items()}


def _extract_projects(section: str) -> list[dict]:
    if not section:
        return []
    chunks = re.split(r"(?<=\.)\s+(?=[A-Z][A-Za-z0-9 &_-]{2,35}(?:\s*[:\-]))", section)
    projects = []
    for chunk in chunks[:12]:
        bits = re.split(r"\s*[:\-]\s*", chunk, maxsplit=1)
        name = bits[0][:80].strip() if bits else "Project"
        description = bits[1].strip() if len(bits) > 1 else chunk.strip()
        if len(description) < 25:
            description = chunk.strip()
        projects.append({"name": name or "Project", "description": description[:800]})
    return projects


def _extract_years(text: str) -> int | None:
    matches = re.findall(r"(?:\b)(\d+)\+?\s*years?", text, re.IGNORECASE)
    return max([int(x) for x in matches], default=0) or None


def parse_resume(text: str) -> dict:
    structured_text = re.sub(r"[ \t]+", " ", text.replace("\x00", " "))
    clean = clean_text(structured_text)
    sections = _sections(structured_text)
    skills = _extract_skills(clean)
    projects = _extract_projects(sections.get("projects", ""))
    certifications = [s.strip() for s in re.split(r"[;|]", sections.get("certifications", "")) if len(s.strip()) > 3][:12]
    education_text = sections.get("education", "")
    experience_text = sections.get("experience", "") or sections.get("work experience", "")
    achievements = [s for s in split_sentences(sections.get("achievements", "")) if s][:12]

    degree_terms = [term for term in ["b.tech", "bachelor", "master", "m.tech", "engineering", "computer science"] if contains_term(clean, term)]
    contact_match = re.search(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b", clean)
    name = contact_match.group(0) if contact_match else None

    evidence_sentences = split_sentences(clean)
    return {
        "name": name,
        "technical_skills": skills,
        "programming_languages": [s for s in skills if s in {"C++", "C", "Python", "Java", "JavaScript", "TypeScript"}],
        "frameworks": [s for s in skills if s in {"React", "Node.js", "FastAPI", "Django", "Flask"}],
        "tools": [s for s in skills if s not in {"C++", "C", "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js", "FastAPI", "Django", "Flask", "Data Structures", "Algorithms", "Machine Learning", "Deep Learning"}],
        "projects": projects,
        "education": {"text": education_text[:1500], "terms": sorted(set(degree_terms))},
        "experience": {"text": experience_text[:3000], "years": _extract_years(experience_text)},
        "certifications": certifications,
        "achievements": achievements,
        "evidence_sentences": evidence_sentences[:80],
        "raw_text": clean[:30000],
    }
