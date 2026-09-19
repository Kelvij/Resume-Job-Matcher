from io import BytesIO
import re
from pypdf import PdfReader


class PDFParseError(ValueError):
    pass


def _normalize_pdf_text(text: str) -> str:
    text = text.replace("\x00", " ")
    lines = []
    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines).strip()


def extract_pdf_text(data: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(data))
        pages: list[str] = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        text = _normalize_pdf_text("\n".join(pages))
    except Exception as exc:
        raise PDFParseError("Unable to read the PDF. Make sure it is a valid, text-based PDF.") from exc
    if len(text) < 60:
        raise PDFParseError("The PDF contains too little extractable text. An OCR step may be required for scanned resumes.")
    return text
