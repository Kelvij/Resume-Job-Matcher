from app.services.jd_parser import parse_jd
from app.services.pdf_parser import PDFParseError, extract_pdf_text
from app.services.resume_parser import parse_resume


def test_invalid_pdf_is_rejected():
    try:
        extract_pdf_text(b"not a pdf")
        assert False, "Expected PDFParseError"
    except PDFParseError:
        pass


def test_empty_inputs_are_safe():
    resume = parse_resume("")
    jd = parse_jd("")
    assert resume["technical_skills"] == []
    assert resume["projects"] == []
    assert jd["required_skills"] == []


def test_missing_resume_sections_are_safe():
    resume = parse_resume("Python SQL")
    assert resume["projects"] == []
    assert resume["certifications"] == []
