from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def health_check() -> dict[str, Any]:
        """Check health of the Polymarket trading API."""
        async with ApiClient() as client:
            return await client.health()
