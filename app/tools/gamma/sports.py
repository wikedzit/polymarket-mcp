from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def get_gamma_sports_metadata() -> dict[str, Any]:
        """Fetch Polymarket sports metadata via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get("/sports/metadata")

    @mcp.tool
    async def get_gamma_sports_market_types() -> list[dict[str, Any]]:
        """Fetch Polymarket sports market types via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get("/sports/market-types")

    @mcp.tool
    async def get_gamma_sports_teams(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Fetch Polymarket sports teams via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/sports/teams",
                {"limit": limit, "offset": offset},
            )
