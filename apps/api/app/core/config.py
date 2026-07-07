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

    # AI Providers
    groq_api_key: str = ""
    gemini_api_key: str = ""

    # Voice Providers (optional — browser TTS is the default)
    elevenlabs_api_key: str = ""
    openai_api_key: str = ""


settings = Settings()
