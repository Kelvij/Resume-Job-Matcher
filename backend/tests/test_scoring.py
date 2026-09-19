from app.services.scoring import coverage_score, education_score, final_score, experience_score


def test_required_coverage():
    assert coverage_score(["C++", "SQL"], ["C++", "SQL", "Python"]) == 1.0
    assert coverage_score(["C++", "SQL"], ["C++"]) == 0.5


def test_experience_alignment():
    resume = {"experience": {"years": 2}}
    assert experience_score(resume, {"experience_years": 1}) == 1.0
    assert experience_score({"experience": {"years": 0}}, {"experience_years": 3}) == 0.25


def test_final_score_weighted():
    result = final_score({"a": 1.0, "b": 0.0}, {"a": 0.75, "b": 0.25})
    assert result == 75


def test_education_alignment():
    resume = {"education": {"text": "B.Tech in Computer Science and Engineering", "terms": ["b.tech", "computer science", "engineering"]}}
    assert education_score(resume, {"education_requirements": ["bachelor", "engineering"]}) == 1.0
