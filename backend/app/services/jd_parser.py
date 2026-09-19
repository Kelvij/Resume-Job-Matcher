import re
from .normalize import SKILL_GROUPS, normalize_skills
from .text_utils import contains_term, split_sentences

REQUIRED_MARKERS = ["required", "must have", "minimum qualifications", "qualifications", "requirements"]
PREFERRED_MARKERS = ["preferred", "nice to have", "bonus", "plus", "preferred qualifications"]
SOFT_SKILLS = ["communication", "collaboration", "leadership", "problem solving", "teamwork", "ownership", "adaptability"]


def _extract_skills(text: str) -> list[str]:
    found: list[str] = []
    lowered = text.lower()
    for canonical, aliases in SKILL_GROUPS.items():
        if any(contains_term(lowered, alias) for alias in aliases):
            found.append(canonical)
    return normalize_skills(found)


def _section_sentences(text: str, markers: list[str]) -> list[str]:
    sentences = split_sentences(text)
    return [s for s in sentences if any(marker in s.lower() for marker in markers)]


def parse_jd(text: str) -> dict:
    clean = text.strip()
    sentences = split_sentences(clean)
    all_skills = _extract_skills(clean)
    required_lines = _section_sentences(clean, REQUIRED_MARKERS)
    preferred_lines = _section_sentences(clean, PREFERRED_MARKERS)
    preferred_skills = [s for s in all_skills if any(s.casefold() in line.casefold() for line in preferred_lines)]
    if required_lines:
        required_skills = [s for s in all_skills if s not in preferred_skills]
    else:
        required_skills = [s for s in all_skills if s not in preferred_skills][: min(8, len(all_skills))]

    experience_years = None
    match = re.search(r"(?:at least|minimum of|around|about)?\s*(\d+)\+?\s*years?", clean, re.IGNORECASE)
    if match:
        experience_years = int(match.group(1))

    education = []
    for term in ["bachelor", "master", "b.tech", "m.tech", "computer science", "engineering", "degree"]:
        if contains_term(clean, term):
            education.append(term)

    soft = [s for s in SOFT_SKILLS if contains_term(clean, s)]
    domain = []
    for term in ["fintech", "healthcare", "e-commerce", "ecommerce", "saas", "robotics", "embedded", "developer tools", "cloud"]:
        if contains_term(clean, term):
            domain.append(term)

    company_name = None
    job_title = None
    first_line = clean.splitlines()[0].strip() if clean.splitlines() else ""
    first_line_match = re.match(r"(.+?)\s+at\s+([A-Z][A-Za-z0-9&.\- ]{2,80})$", first_line, re.IGNORECASE)
    if first_line_match:
        job_title = first_line_match.group(1).strip(" —-")
        company_name = first_line_match.group(2).strip(" .,")
    company_match = re.search(r"(?:at|for)\s+([A-Z][A-Za-z0-9&.-]{2,}(?:\s+[A-Z][A-Za-z0-9&.-]{2,}){0,3})", clean)
    if company_match and not company_name:
        company_name = company_match.group(1).strip(" .,")

    title_match = re.search(r"(?:job title|position|role)\s*[:\-]\s*([^\n.]{3,80})", clean, re.IGNORECASE)
    if title_match:
        job_title = title_match.group(1).strip()

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "tools_technologies": all_skills,
        "education_requirements": sorted(set(education)),
        "experience_years": experience_years,
        "soft_skills": sorted(set(soft)),
        "domain_requirements": sorted(set(domain)),
        "requirement_sentences": sentences[:30],
        "company_name": company_name,
        "job_title": job_title,
        "raw_text": clean[:24000],
    }
