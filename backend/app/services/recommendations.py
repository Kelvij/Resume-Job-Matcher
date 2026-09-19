def build_recommendations(gaps: list[dict], projects: list[dict]) -> list[dict]:
    recommendations = []
    for gap in gaps[:8]:
        recommendations.append({
            "action": f"Address {gap['skill']} only if you genuinely have relevant experience.",
            "basis": gap["why_it_matters"],
            "evidence_type": "job_requirement",
            "evidence": gap["skill"],
        })
    if projects:
        top_project = max(projects, key=lambda x: x["relevance_score"])
        recommendations.append({
            "action": "Move the most relevant project higher in the resume when it directly demonstrates the target requirements.",
            "basis": "Project relevance is a scored component of this report.",
            "evidence_type": "analysis_signal",
            "evidence": top_project["name"],
        })
    recommendations.append({
        "action": "Add measurable outcomes only where the original work actually has verifiable numbers.",
        "basis": "Quantified impact can make existing evidence clearer without inventing credentials.",
        "evidence_type": "resume_editing",
        "evidence": "Existing project/experience bullets",
    })
    return recommendations
