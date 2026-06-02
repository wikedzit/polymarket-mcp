from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def list_gamma_series(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List Polymarket series via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get("/series", {"limit": limit, "offset": offset})

    @tool
    async def get_gamma_series(series_id: str) -> dict[str, Any]:
        """Fetch a Polymarket series by ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/series/{series_id}")
