import re
from collections import defaultdict

SKILL_GROUPS = {
    "C++": ["c++", "cpp", "c plus plus"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node", "node.js", "nodejs"],
    "PostgreSQL": ["postgres", "postgresql"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "REST APIs": ["rest api", "rest apis", "restful api", "restful apis", "rest"],
    "Object-Oriented Programming": ["object oriented programming", "object-oriented programming", "oop", "object oriented design", "object-oriented design"],
    "Data Structures": ["data structures", "data structure", "ds"],
    "Algorithms": ["algorithms", "algorithm", "dsa", "data structures and algorithms"],
    "AWS": ["aws", "amazon web services"],
    "Docker": ["docker", "containerization", "containers"],
    "Git": ["git", "github", "gitlab"],
    "SQL": ["sql", "structured query language"],
    "Python": ["python"],
    "Java": ["java"],
    "C": ["c programming", "c language"],
    "FastAPI": ["fastapi", "fast api"],
    "Django": ["django"],
    "Flask": ["flask"],
    "MongoDB": ["mongodb", "mongo db"],
    "Redis": ["redis"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous delivery", "continuous deployment"],
    "Linux": ["linux", "ubuntu"],
    "Postman": ["postman"],
    "Figma": ["figma"],
}

_ALIAS_TO_CANONICAL = {
    alias: canonical
    for canonical, aliases in SKILL_GROUPS.items()
    for alias in aliases
}


def normalize_skill(raw: str) -> str:
    text = re.sub(r"\s+", " ", raw.lower().strip())
    return _ALIAS_TO_CANONICAL.get(text, raw.strip())


def normalize_skills(skills: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for skill in skills:
        normalized = normalize_skill(skill)
        key = normalized.casefold()
        if key not in seen:
            seen.add(key)
            out.append(normalized)
    return out


def canonical_skill_lookup() -> dict[str, list[str]]:
    return defaultdict(list, SKILL_GROUPS)
