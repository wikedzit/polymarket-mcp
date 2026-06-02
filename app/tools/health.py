from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient
from app.tools.helpers import make_tool


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def health_check() -> dict[str, Any]:
        """Check health of the Polymarket trading API."""
        async with ApiClient() as client:
            return await client.health()
