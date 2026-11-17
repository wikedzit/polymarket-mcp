from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    polymarket_api_url: str = "http://127.0.0.1:8005"
    polymarket_api_access_token: str | None = None

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
    http_timeout_seconds: int = 60

    @field_validator("ask_execute_confidence", "ask_clarify_confidence")
    @classmethod
    def validate_confidence_range(cls, value: float) -> float:
        if not 0 <= value <= 1:
            raise ValueError("confidence must be between 0 and 1 inclusive")
        return value

    @field_validator("ask_session_ttl_seconds", "http_timeout_seconds")
    @classmethod
    def validate_at_least_one_second(cls, value: int) -> int:
        if value < 1:
            raise ValueError("must be at least 1 second")
        return value

    @model_validator(mode="after")
    def validate_execute_ge_clarify(self) -> "Settings":
        if self.ask_execute_confidence < self.ask_clarify_confidence:
            raise ValueError(
                "ask_execute_confidence must be greater than or equal to "
                "ask_clarify_confidence"
            )
        return self

    @field_validator("mcp_url", "polymarket_api_url", "openai_base_url", mode="before")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")


settings = Settings()
