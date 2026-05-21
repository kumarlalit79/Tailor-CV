from functools import lru_cache
from pathlib import Path

from pydantic.v1 import BaseSettings, Field

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"
DEFAULT_OPENAI_BASE_URL = "https://models.inference.ai.azure.com"


class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    openai_base_url: str = Field(
        default=DEFAULT_OPENAI_BASE_URL,
        env="OPENAI_BASE_URL",
    )
    frontend_url: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    pdf_output_dir: str = Field(default="generated/temp", env="PDF_OUTPUT_DIR")
    environment: str = Field(default="development", env="ENVIRONMENT")

    @property
    def cors_origins(self) -> list[str]:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

        if self.frontend_url and self.frontend_url not in origins:
            origins.append(self.frontend_url)

        return origins

    @property
    def resolved_openai_base_url(self) -> str:
        return self.openai_base_url.strip() or DEFAULT_OPENAI_BASE_URL

    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
