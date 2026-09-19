from app.services.demo import DEMO_JD, DEMO_RESUME
from app.services.jd_parser import parse_jd
from app.services.resume_parser import parse_resume
import app.services.report as report_service
from app.services.report import build_report


def test_report_is_explainable(monkeypatch):
    monkeypatch.setattr(report_service, "semantic_similarity", lambda *args, **kwargs: 0.72)
    monkeypatch.setattr(report_service, "best_sentence_similarity", lambda query, candidates, model_name: (0.80, candidates[0] if candidates else None))
    monkeypatch.setattr(report_service, "score_projects", lambda projects, jd, model_name: [{"name": "Demo", "relevance_score": 75, "level": "High", "reasons": ["test"], "evidence": "test"}])
    report = build_report(parse_resume(DEMO_RESUME), parse_jd(DEMO_JD), "sentence-transformers/all-MiniLM-L6-v2", {
        "required_skills": 0.4,
        "preferred_skills": 0.15,
        "semantic_relevance": 0.2,
        "experience_alignment": 0.15,
        "project_relevance": 0.1,
        "education_alignment": 0.05,
    })
    assert 0 <= report["overall_score"] <= 100
    assert "score_components" in report
    assert "recommendations" in report
    assert all("basis" in rec for rec in report["recommendations"])
