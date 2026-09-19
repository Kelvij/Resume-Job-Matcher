import httpx


class LLMError(RuntimeError):
    pass


async def enrich_report(report: dict, api_key: str | None, base_url: str, model: str, enabled: bool) -> dict:
    if not enabled or not api_key:
        return report

    system = (
        "You are an evidence-grounded resume analyst. Return JSON only. "
        "Do not invent experience, skills, projects, achievements, or metrics. "
        "Every recommendation must reference supplied resume evidence or a supplied job requirement."
    )
    payload = {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": (
                "Enhance this already-computed report with a concise executive summary, "
                "evidence-grounded explanations, and actionable suggestions. Never change the score. "
                "Return keys: executive_summary, recommendation_explanations, rewritten_bullets.\n\n"
                + str(report)
            )},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                base_url.rstrip("/") + "/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
            )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        import json
        additions = json.loads(content)
        if isinstance(additions, dict):
            report["llm_enrichment"] = additions
    except Exception as exc:
        report["llm_enrichment"] = {"status": "unavailable", "message": "Optional explanation service unavailable."}
    return report
