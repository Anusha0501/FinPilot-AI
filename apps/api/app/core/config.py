from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinPilot-AI API"
    database_url: str = "sqlite:///./finpilot.db"
    upload_dir: str = "./uploads"
    max_upload_mb: int = 10
    google_api_key: str | None = None
    langsmith_tracing: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
