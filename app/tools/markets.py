from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def list_active_events(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List active Polymarket events via the trading API."""
        async with ApiClient() as client:
            return await client.list_active_events(limit=limit, offset=offset)

    @mcp.tool
    async def get_market_by_slug(slug: str) -> dict[str, Any]:
        """Fetch a Polymarket market by URL slug via the trading API."""
        async with ApiClient() as client:
            return await client.get_market_by_slug(slug)

    @mcp.tool
    async def list_active_markets(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List active Polymarket markets via the trading API."""
        async with ApiClient() as client:
            return await client.list_active_markets(limit=limit, offset=offset)

    @mcp.tool
    async def get_markets_by_condition_ids(
        condition_ids: list[str],
    ) -> list[dict[str, Any]]:
        """Fetch Polymarket markets by condition IDs via the trading API."""
        async with ApiClient() as client:
            return await client.get_markets_by_condition_ids(condition_ids)
