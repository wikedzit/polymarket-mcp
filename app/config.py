from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    polymarket_api_url: str = "http://127.0.0.1:8000"


settings = Settings()
