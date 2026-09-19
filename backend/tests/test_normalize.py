from app.services.normalize import normalize_skill, normalize_skills


def test_aliases_normalize():
    assert normalize_skill("CPP") == "C++"
    assert normalize_skill("Postgres") == "PostgreSQL"
    assert normalize_skill("ML") == "Machine Learning"


def test_duplicate_skills_removed():
    assert normalize_skills(["JS", "JavaScript", "javascript"]) == ["JavaScript"]
