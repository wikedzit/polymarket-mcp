from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    polymarket_api_url: str = "http://127.0.0.1:8000"

    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8001
    mcp_url: str = "http://127.0.0.1:8001"
    mcp_auth_token: str | None = None
    mcp_stateless_http: bool = True

    # Natural-language ask router (OpenAI)
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    ask_session_ttl_seconds: int = 1800
    ask_execute_confidence: float = 0.75
    ask_clarify_confidence: float = 0.4

    @field_validator("mcp_url", "polymarket_api_url", "openai_base_url", mode="before")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")


settings = Settings()
