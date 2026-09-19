from .embeddings import best_sentence_similarity
from .normalize import normalize_skill


def score_projects(projects: list[dict], jd: dict, model_name: str) -> list[dict]:
    target_skills = jd.get("required_skills", []) + jd.get("preferred_skills", [])
    jd_text = " ".join(jd.get("requirement_sentences", []))
    results = []
    for project in projects:
        description = project.get("description", "")
        semantic, evidence = best_sentence_similarity(description, [jd_text] if jd_text else [], model_name)
        skill_hits = []
        lower_desc = description.casefold()
        for skill in target_skills:
            if normalize_skill(skill).casefold() in lower_desc:
                skill_hits.append(skill)
        coverage = len(set(skill_hits)) / len(set(target_skills)) if target_skills else 0.0
        combined = min(1.0, semantic * 0.65 + coverage * 0.35)
        level = "High" if combined >= 0.72 else "Medium" if combined >= 0.45 else "Low"
        reasons = []
        if semantic >= 0.6:
            reasons.append("Semantic overlap with the job requirements")
        if skill_hits:
            reasons.append("Uses: " + ", ".join(skill_hits[:5]))
        if not reasons:
            reasons.append("Limited direct evidence for the target requirements")
        results.append({
            "name": project.get("name", "Project"),
            "relevance_score": round(combined * 100),
            "level": level,
            "reasons": reasons,
            "evidence": evidence,
        })
    return results
