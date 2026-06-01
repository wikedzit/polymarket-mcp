from typing import Any, Literal

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def clob_server_time() -> Any:
        """Get CLOB server time via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/time")

    @mcp.tool
    async def get_clob_orderbook(token_id: str) -> Any:
        """Get CLOB orderbook via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/orderbook", {"token_id": token_id})

    @mcp.tool
    async def get_clob_midpoint(token_id: str) -> Any:
        """Get CLOB midpoint via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/midpoint", {"token_id": token_id})

    @mcp.tool
    async def get_clob_spread(token_id: str) -> Any:
        """Get CLOB spread via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/spread", {"token_id": token_id})

    @mcp.tool
    async def get_clob_price(
        token_id: str,
        side: Literal["BUY", "SELL"],
    ) -> Any:
        """Get CLOB best bid or ask via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/price", {"token_id": token_id, "side": side})

    @mcp.tool
    async def get_clob_tick_size(token_id: str) -> Any:
        """Get CLOB tick size via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/tick-size", {"token_id": token_id})

    @mcp.tool
    async def get_clob_neg_risk(token_id: str) -> Any:
        """Get CLOB neg-risk flag via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/neg-risk", {"token_id": token_id})

    @mcp.tool
    async def get_clob_fee_rate(token_id: str) -> Any:
        """Get CLOB fee rate via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/fee-rate", {"token_id": token_id})

    @mcp.tool
    async def get_clob_last_trade_price(token_id: str) -> Any:
        """Get CLOB last trade price via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get("/last-trade-price", {"token_id": token_id})
