from functools import lru_cache
import re
import numpy as np


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9+#.]+", text.lower())


def _fallback_embedding(text: str) -> dict[str, float]:
    counts: dict[str, float] = {}
    for token in _tokens(text):
        counts[token] = counts.get(token, 0.0) + 1.0
    norm = sum(v * v for v in counts.values()) ** 0.5 or 1.0
    return {k: v / norm for k, v in counts.items()}


@lru_cache(maxsize=1)
def get_model(model_name: str):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return float(np.dot(a, b) / (a_norm * b_norm))


def _fallback_similarity(text_a: str, text_b: str) -> float:
    a, b = _fallback_embedding(text_a), _fallback_embedding(text_b)
    if not a or not b:
        return 0.0
    return max(0.0, min(1.0, sum(v * b.get(k, 0.0) for k, v in a.items())))


def semantic_similarity(text_a: str, text_b: str, model_name: str) -> float:
    text_a = text_a[:6000].strip()
    text_b = text_b[:6000].strip()
    if not text_a or not text_b:
        return 0.0
    try:
        model = get_model(model_name)
        embeddings = model.encode([text_a, text_b], normalize_embeddings=True)
        score = float(np.dot(embeddings[0], embeddings[1]))
        return max(0.0, min(1.0, score))
    except Exception:
        return _fallback_similarity(text_a, text_b)


def best_sentence_similarity(query: str, candidates: list[str], model_name: str) -> tuple[float, str | None]:
    if not query or not candidates:
        return 0.0, None
    try:
        model = get_model(model_name)
        q = model.encode([query], normalize_embeddings=True)[0]
        c = model.encode(candidates[:100], normalize_embeddings=True)
        scores = c @ q
        idx = int(np.argmax(scores))
        return max(0.0, min(1.0, float(scores[idx]))), candidates[idx]
    except Exception:
        scores = [_fallback_similarity(query, candidate) for candidate in candidates[:100]]
        idx = int(np.argmax(scores))
        return scores[idx], candidates[idx]
