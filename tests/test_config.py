from app.config import Settings


def test_settings_urls_strip_trailing_slash() -> None:
    settings = Settings(
        mcp_url="http://127.0.0.1:8001/",
        polymarket_api_url="http://127.0.0.1:8005/",
        openai_base_url="https://api.openai.com/v1/",
    )
    assert settings.mcp_url == "http://127.0.0.1:8001"
    assert settings.polymarket_api_url == "http://127.0.0.1:8005"
    assert settings.openai_base_url == "https://api.openai.com/v1"