from fastmcp import FastMCP
from fastmcp.server.auth import StaticTokenVerifier

from app.config import settings
from app.middleware.structured_response import StructuredResponseMiddleware
from app.tools import register_tools


def create_mcp() -> FastMCP:
    auth = None
    if settings.mcp_auth_token:
        auth = StaticTokenVerifier(
            tokens={settings.mcp_auth_token: {"sub": "client", "client_id": "http-client"}}
        )

    instructions = (
        "MCP server for Polymarket trading operations. "
        "All tools proxy requests to the local Polymarket trading API. "
        "Every tool returns a structured envelope: {ok, data, error}. "
        "Use the `ask` tool for natural-language requests — pass your text in `query` "
        "and reuse `session_id` when disambiguating tool choices."
    )
    server = FastMCP(
        "Polymarket MCP",
        instructions=instructions,
        version="0.1.0",
        auth=auth,
    )
    register_tools(server)
    server.add_middleware(StructuredResponseMiddleware())
    return server


mcp = create_mcp()


if __name__ == "__main__":
    mcp.run()
