from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def get_clob_api_keys() -> Any:
        """List CLOB API keys via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/auth/api-keys")

    @tool
    async def get_clob_closed_only_mode() -> Any:
        """Get CLOB closed-only ban status via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/auth/ban-status/closed-only")

    @tool
    async def get_clob_builder_api_keys() -> Any:
        """List CLOB builder API keys via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/auth/builder-api-key")

    @tool
    async def get_clob_notifications() -> Any:
        """Get CLOB notifications via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/notifications")

    @tool
    async def get_clob_rewards_user(date: str | None = None) -> Any:
        """Get CLOB user rewards for a day via the trading API."""
        params = {"date": date} if date else None
        async with ApiClient() as client:
            return await client.clob_get("/rewards/user", params)

    @tool
    async def get_clob_rewards_markets_current() -> Any:
        """Get current CLOB reward markets via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/rewards/markets/current")

    @tool
    async def get_clob_builder_trades(
        market: str | None = None,
        asset_id: str | None = None,
    ) -> Any:
        """Get builder-attributed CLOB trades via the trading API."""
        params: dict[str, Any] = {}
        if market:
            params["market"] = market
        if asset_id:
            params["asset_id"] = asset_id
        async with ApiClient() as client:
            return await client.clob_get("/builder/trades", params or None)
