from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def data_health() -> dict[str, Any]:
        """Check Polymarket Data API health via the trading API."""
        async with ApiClient() as client:
            return await client.data_get("/")

    @mcp.tool
    async def get_data_positions(
        user: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get open positions for a wallet via the trading API Data service."""
        async with ApiClient() as client:
            return await client.data_get(
                "/positions",
                {"user": user, "limit": limit, "offset": offset},
            )

    @mcp.tool
    async def get_data_closed_positions(
        user: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get closed positions for a wallet via the trading API."""
        async with ApiClient() as client:
            return await client.data_get(
                "/closed-positions",
                {"user": user, "limit": limit, "offset": offset},
            )

    @mcp.tool
    async def get_data_value(user: str) -> list[dict[str, Any]]:
        """Get total USDC value of a wallet's positions via the trading API."""
        async with ApiClient() as client:
            return await client.data_get("/value", {"user": user})

    @mcp.tool
    async def get_data_trades(
        market: str | None = None,
        user: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get trade history via the trading API Data service."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if market:
            params["market"] = market
        if user:
            params["user"] = user
        async with ApiClient() as client:
            return await client.data_get("/trades", params)

    @mcp.tool
    async def get_data_activity(
        user: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get on-chain activity for a wallet via the trading API."""
        async with ApiClient() as client:
            return await client.data_get(
                "/activity",
                {"user": user, "limit": limit, "offset": offset},
            )

    @mcp.tool
    async def get_data_holders(
        market: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get top holders for a market condition ID via the trading API."""
        async with ApiClient() as client:
            return await client.data_get("/holders", {"market": market, "limit": limit})

    @mcp.tool
    async def get_data_traded(user: str) -> dict[str, Any]:
        """Get count of markets traded by a wallet via the trading API."""
        async with ApiClient() as client:
            return await client.data_get("/traded", {"user": user})
