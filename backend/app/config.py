from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Resume–Job Matcher API"
    api_prefix: str = "/api"
    database_url: str = "postgresql+psycopg://resume_matcher:resume_matcher@localhost:5432/resume_matcher"
    frontend_origin: str = "http://localhost:5173"
    max_resume_bytes: int = 5 * 1024 * 1024
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_enabled: bool = False
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"
    score_weights: dict[str, float] = {
        "required_skills": 0.35,
        "preferred_skills": 0.15,
        "semantic_relevance": 0.20,
        "experience_alignment": 0.15,
        "project_relevance": 0.10,
        "education_alignment": 0.05,
    }

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
