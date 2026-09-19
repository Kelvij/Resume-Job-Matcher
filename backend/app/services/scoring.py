def coverage_score(required: list[str], candidate: list[str]) -> float:
    if not required:
        return 1.0
    candidate_set = {x.casefold() for x in candidate}
    hits = sum(1 for skill in required if skill.casefold() in candidate_set)
    return hits / len(required)


def experience_score(resume: dict, jd: dict) -> float:
    required = jd.get("experience_years")
    actual = resume.get("experience", {}).get("years") or 0
    if not required:
        return 1.0 if actual > 0 else 0.55
    if actual >= required:
        return 1.0
    if actual == 0:
        return 0.25
    return min(0.95, actual / required)


def project_score(projects: list[dict]) -> float:
    if not projects:
        return 0.25
    return sum(p["relevance_score"] for p in projects) / (100 * len(projects))


def final_score(components: dict[str, float], weights: dict[str, float]) -> int:
    weighted = sum(components.get(k, 0.0) * weights.get(k, 0.0) for k in weights)
    return max(0, min(100, round(weighted * 100)))


def education_score(resume: dict, jd: dict) -> float:
    required = [x.casefold() for x in jd.get("education_requirements", [])]
    if not required:
        return 0.6
    resume_text = (resume.get("education", {}).get("text", "") + " " + " ".join(resume.get("education", {}).get("terms", []))).casefold()
    equivalents = {
        "bachelor": ["bachelor", "b.tech", "btech", "undergraduate", "degree"],
        "master": ["master", "m.tech", "mtech", "postgraduate"],
        "computer science": ["computer science", "cs"],
        "engineering": ["engineering", "engineer", "b.tech", "m.tech"],
        "degree": ["degree", "bachelor", "master", "b.tech", "m.tech"],
    }
    hits = 0
    for term in required:
        aliases = equivalents.get(term, [term])
        if any(alias in resume_text for alias in aliases):
            hits += 1
    return hits / len(required) if hits else 0.0
