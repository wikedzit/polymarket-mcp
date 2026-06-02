from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def get_data_open_interest(market: str | None = None) -> dict[str, Any]:
        """Get open interest via the trading API Data service."""
        params = {"market": market} if market else None
        async with ApiClient() as client:
            return await client.data_get("/oi", params)

    @tool
    async def get_data_live_volume(event_id: int) -> dict[str, Any]:
        """Get live event volume via the trading API Data service."""
        async with ApiClient() as client:
            return await client.data_get("/live-volume", {"id": event_id})

    @tool
    async def get_data_market_positions(
        market: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get all positions for a market via the trading API."""
        async with ApiClient() as client:
            return await client.data_get(
                "/v1/market-positions",
                {"market": market, "limit": limit, "offset": offset},
            )
