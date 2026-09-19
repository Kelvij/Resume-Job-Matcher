from .embeddings import semantic_similarity, best_sentence_similarity
from .normalize import normalize_skill
from .project_relevance import score_projects
from .recommendations import build_recommendations
from .scoring import coverage_score, education_score, experience_score, project_score, final_score


def find_skill_evidence(skill: str, sentences: list[str]) -> str | None:
    skill_norm = normalize_skill(skill).casefold()
    aliases = {
        "c++": ["c++", "cpp"],
        "javascript": ["javascript", "js"],
        "react": ["react", "react.js", "reactjs"],
        "postgresql": ["postgres", "postgresql"],
        "machine learning": ["machine learning", "ml"],
        "rest apis": ["rest api", "restful api", "rest"],
    }.get(skill_norm, [skill])
    for sentence in sentences:
        low = sentence.casefold()
        if any(alias in low for alias in aliases):
            return sentence[:350]
    return None


def build_report(resume: dict, jd: dict, model_name: str, weights: dict[str, float]) -> dict:
    resume_skills = resume.get("technical_skills", [])
    required = jd.get("required_skills", [])
    preferred = jd.get("preferred_skills", [])
    matched = []
    partial = []
    missing = []
    resume_sentences = resume.get("evidence_sentences", [])

    for skill in required:
        evidence = find_skill_evidence(skill, resume_sentences)
        if skill.casefold() in {x.casefold() for x in resume_skills}:
            matched.append({"skill": skill, "status": "matched", "evidence": evidence})
        else:
            similarity, evidence_sim = best_sentence_similarity(skill, resume_sentences, model_name)
            if similarity >= 0.58:
                partial.append({"skill": skill, "status": "partial", "evidence": evidence_sim})
            else:
                missing.append({"skill": skill, "status": "missing", "evidence": None})

    preferred_match = []
    for skill in preferred:
        evidence = find_skill_evidence(skill, resume_sentences)
        preferred_match.append({"skill": skill, "matched": evidence is not None, "evidence": evidence})

    jd_text = " ".join(jd.get("requirement_sentences", []))
    semantic = semantic_similarity(resume.get("raw_text", ""), jd_text, model_name)
    projects = score_projects(resume.get("projects", []), jd, model_name)
    exp = experience_score(resume, jd)
    edu = education_score(resume, jd)
    components = {
        "required_skills": coverage_score(required, resume_skills),
        "preferred_skills": coverage_score(preferred, resume_skills),
        "semantic_relevance": semantic,
        "experience_alignment": exp,
        "project_relevance": project_score(projects),
        "education_alignment": edu,
    }
    score = final_score(components, weights)

    gaps = []
    for item in missing:
        gaps.append({"priority": "High", "skill": item["skill"], "why_it_matters": "Listed as a required job skill but no supporting resume evidence was found."})
    for item in preferred_match:
        if not item["matched"]:
            gaps.append({"priority": "Low", "skill": item["skill"], "why_it_matters": "Listed as a preferred skill; adding genuine evidence could strengthen alignment."})

    recommendations = build_recommendations(gaps, projects)

    return {
        "overall_score": score,
        "score_components": {
            key: {"score": round(value * 100), "weight": round(weights.get(key, 0) * 100), "contribution": round(value * weights.get(key, 0) * 100)}
            for key, value in components.items()
        },
        "matched_skills": matched,
        "partial_skills": partial,
        "missing_skills": missing,
        "preferred_skills": preferred_match,
        "skill_summary": {
            "matched_count": len(matched),
            "partial_count": len(partial),
            "missing_count": len(missing),
        },
        "job_requirements": {
            "required_skills": required,
            "preferred_skills": preferred,
            "tools_technologies": jd.get("tools_technologies", []),
            "education_requirements": jd.get("education_requirements", []),
            "experience_years": jd.get("experience_years"),
            "soft_skills": jd.get("soft_skills", []),
            "domain_requirements": jd.get("domain_requirements", []),
        },
        "resume_analysis": {
            "technical_skills": resume.get("technical_skills", []),
            "programming_languages": resume.get("programming_languages", []),
            "frameworks": resume.get("frameworks", []),
            "tools": resume.get("tools", []),
            "education": resume.get("education", {}),
            "experience": resume.get("experience", {}),
            "certifications": resume.get("certifications", []),
            "achievements": resume.get("achievements", []),
        },
        "project_relevance": projects,
        "experience_alignment": {
            "resume_years": resume.get("experience", {}).get("years"),
            "required_years": jd.get("experience_years"),
            "score": round(exp * 100),
            "explanation": "Based on extracted experience duration; no inference is made about unlisted work."
        },
        "skill_gap_analysis": {"high_priority": [g for g in gaps if g["priority"] == "High"], "low_priority": [g for g in gaps if g["priority"] == "Low"]},
        "recommendations": recommendations,
        "semantic_evidence": {
            "resume_to_jd_similarity": round(semantic * 100),
            "note": "Semantic similarity contributes a configurable component but does not determine the final score by itself."
        },
        "education_alignment": {
            "score": round(edu * 100),
            "explanation": "Based only on explicit education evidence extracted from the resume and education requirements detected in the JD."
        },
    }
