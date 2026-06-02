from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def get_clob_simplified_markets(next_cursor: str | None = None) -> Any:
        """List CLOB simplified markets via the trading API."""
        params = {"next_cursor": next_cursor} if next_cursor else None
        async with ApiClient() as client:
            return await client.clob_get("/markets/simplified", params)

    @tool
    async def get_clob_market_info(condition_id: str) -> Any:
        """Get CLOB market info for a condition ID via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get(f"/clob-markets/{condition_id}")

    @tool
    async def get_clob_market_by_token(token_id: str) -> Any:
        """Resolve CLOB market by outcome token ID via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get(f"/markets-by-token/{token_id}")

    @tool
    async def get_clob_live_activity(condition_id: str) -> Any:
        """Get CLOB live activity for a market via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get(f"/markets/live-activity/{condition_id}")
