from typing import Any, Literal

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def clob_server_time() -> dict[str, int]:
        """Return Polymarket CLOB server time via the trading API."""
        async with ApiClient() as client:
            return await client.clob_server_time()

    @mcp.tool
    async def get_orderbook(token_id: str) -> dict[str, Any]:
        """Fetch the CLOB orderbook for an outcome token ID via the trading API."""
        async with ApiClient() as client:
            return await client.get_orderbook(token_id)

    @mcp.tool
    async def get_midpoint(token_id: str) -> dict[str, str]:
        """Fetch the CLOB midpoint price via the trading API."""
        async with ApiClient() as client:
            return await client.get_midpoint(token_id)

    @mcp.tool
    async def get_spread(token_id: str) -> dict[str, str]:
        """Fetch the CLOB bid-ask spread via the trading API."""
        async with ApiClient() as client:
            return await client.get_spread(token_id)

    @mcp.tool
    async def get_price(
        token_id: str,
        side: Literal["BUY", "SELL"],
    ) -> dict[str, str]:
        """Fetch the best CLOB bid or ask via the trading API."""
        async with ApiClient() as client:
            return await client.get_price(token_id, side)

    @mcp.tool
    async def get_tick_size(token_id: str) -> dict[str, str]:
        """Fetch the minimum tick size via the trading API."""
        async with ApiClient() as client:
            return await client.get_tick_size(token_id)
