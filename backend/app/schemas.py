from datetime import datetime
from pydantic import BaseModel, Field


class AnalysisSummary(BaseModel):
    id: str
    resume_name: str
    company_name: str | None = None
    job_title: str | None = None
    score: int = Field(ge=0, le=100)
    created_at: datetime


class AnalysisResponse(BaseModel):
    id: str | None = None
    demo: bool = False
    resume_name: str
    company_name: str | None = None
    job_title: str | None = None
    report: dict


class DemoResponse(AnalysisResponse):
    demo: bool = True
