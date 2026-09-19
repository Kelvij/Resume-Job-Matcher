import re


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    clean = clean_text(text)
    if not clean:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean) if s.strip()]


def contains_term(text: str, term: str) -> bool:
    pattern = re.escape(term).replace(r"\ ", r"\s+")
    return re.search(rf"(?<!\w){pattern}(?!\w)", text, re.IGNORECASE) is not None
