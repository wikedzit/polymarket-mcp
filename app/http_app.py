from starlette.responses import JSONResponse

from app.config import settings
from app.main import mcp


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "healthy",
            "service": "polymarket-mcp",
        }
    )


app = mcp.http_app(stateless_http=settings.mcp_stateless_http)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "app.http_app:app",
        host=settings.mcp_host,
        port=settings.mcp_port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
