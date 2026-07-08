from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Financial Copilot"
    app_env: str = "development"
    secret_key: str = "change-me-in-production"
    cors_origins: str = "http://localhost:3000"

    database_url: str = "postgresql+asyncpg://copilot:copilot@localhost:5432/ai_financial_copilot"
    redis_url: str = "redis://localhost:6379/0"

    alpha_vantage_api_key: str = ""
    fmp_api_key: str = ""
    polygon_api_key: str = ""
    twelve_data_api_key: str = ""

    anthropic_api_key: str = ""
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    llm_provider: str = "anthropic"
    llm_model: str = "claude-3-5-haiku-20241022"
    embedding_model: str = "text-embedding-3-small"

    vector_store_path: str = "./data/vector_store"
    chroma_persist_dir: str = "./data/chroma"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
