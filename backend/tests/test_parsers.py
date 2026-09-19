from app.services.jd_parser import parse_jd
from app.services.resume_parser import parse_resume


def test_jd_related_terms():
    jd = parse_jd("Required: C++ and Object-Oriented Design. Preferred: ML and Postgres.")
    assert "C++" in jd["tools_technologies"]
    assert "Object-Oriented Programming" in jd["tools_technologies"]
    assert "Machine Learning" in jd["tools_technologies"]
    assert "PostgreSQL" in jd["tools_technologies"]


def test_resume_missing_sections_is_safe():
    resume = parse_resume("A short resume. Skills Python and SQL. Education B.Tech.")
    assert "Python" in resume["technical_skills"]
    assert resume["projects"] == []
