from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    app_name: str = "KitchenKavach"
    environment: str = "local"

    # Primary LLM
    llm_api_key: str = ""
    llm_base_url: str = ""
    primary_model: str = ""

    # Fallback LLM
    fallback_api_key: str = ""
    fallback_base_url: str = ""
    fallback_model: str = ""

    llm_timeout_seconds: int = 20


@lru_cache
def get_settings() -> Settings:
    return Settings()