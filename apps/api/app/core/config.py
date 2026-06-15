from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_name: str = "LifeOS API"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/lifeos"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # CORS — comma-separated origins
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
