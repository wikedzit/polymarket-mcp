from typing import Any, Literal

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def gamma_search(
        q: str,
        search_type: Literal["markets", "events", "profiles"] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search Polymarket markets, events, or profiles via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_search(q, search_type, limit)
