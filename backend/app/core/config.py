from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar, Any

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume Optimizer API"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"  # Defaults to SQLite for testing
    
    # LLM APIs
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
