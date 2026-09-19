import os
from pathlib import Path
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import get_settings
from .database import Base, engine, get_db
from .models import Analysis
from .schemas import AnalysisResponse, AnalysisSummary, DemoResponse
from .services.demo import demo_report
from .services.jd_parser import parse_jd
from .services.llm import enrich_report
from .services.pdf_parser import PDFParseError, extract_pdf_text
from .services.report import build_report
from .services.resume_parser import parse_resume

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-resume-job-matcher"}


@app.post(f"{settings.api_prefix}/analyze", response_model=AnalysisResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF resumes are supported.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
    if len(job_description) > 30000:
        raise HTTPException(status_code=413, detail="Job description is too large.")

    data = await resume.read()
    if not data.startswith(b"%PDF"):
        raise HTTPException(status_code=415, detail="The uploaded file is not a valid PDF document.")
    if len(data) > settings.max_resume_bytes:
        raise HTTPException(status_code=413, detail="Resume PDF exceeds the configured size limit.")
    try:
        resume_text = extract_pdf_text(data)
    except PDFParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    resume_info = parse_resume(resume_text)
    jd_info = parse_jd(job_description)
    report = build_report(resume_info, jd_info, settings.embedding_model, settings.score_weights)
    report = await enrich_report(report, settings.llm_api_key, settings.llm_base_url, settings.llm_model, settings.llm_enabled)

    analysis = Analysis(
        resume_name=resume.filename or "resume.pdf",
        company_name=jd_info.get("company_name"),
        job_title=jd_info.get("job_title"),
        score=report["overall_score"],
        report=report,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return AnalysisResponse(id=analysis.id, resume_name=analysis.resume_name, company_name=analysis.company_name, job_title=analysis.job_title, report=analysis.report)


@app.get(f"{settings.api_prefix}/demo", response_model=DemoResponse)
async def demo() -> DemoResponse:
    report = demo_report(settings.embedding_model, settings.score_weights)
    return DemoResponse(resume_name="demo_resume.pdf", company_name="Nova Systems", job_title="Software Engineer — Developer Platform", report=report)


@app.get(f"{settings.api_prefix}/history", response_model=list[AnalysisSummary])
def history(db: Session = Depends(get_db)) -> list[AnalysisSummary]:
    rows = db.execute(select(Analysis).order_by(Analysis.created_at.desc()).limit(50)).scalars().all()
    return [AnalysisSummary(id=row.id, resume_name=row.resume_name, company_name=row.company_name, job_title=row.job_title, score=row.score, created_at=row.created_at) for row in rows]


@app.get(f"{settings.api_prefix}/history/{{analysis_id}}", response_model=AnalysisResponse)
def get_history(analysis_id: str, db: Session = Depends(get_db)) -> AnalysisResponse:
    row = db.get(Analysis, analysis_id)
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return AnalysisResponse(id=row.id, resume_name=row.resume_name, company_name=row.company_name, job_title=row.job_title, report=row.report)


@app.delete(f"{settings.api_prefix}/history/{{analysis_id}}", status_code=204)
def delete_history(analysis_id: str, db: Session = Depends(get_db)) -> None:
    row = db.get(Analysis, analysis_id)
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    db.delete(row)
    db.commit()
