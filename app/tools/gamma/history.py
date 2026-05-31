from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def get_gamma_prices_history(
        market: str,
        fidelity: int | None = None,
        interval: str | None = None,
        start_ts: int | None = None,
        end_ts: int | None = None,
    ) -> dict[str, Any]:
        """Fetch historical prices for a token via the trading API."""
        params: dict[str, Any] = {"market": market}
        if fidelity is not None:
            params["fidelity"] = fidelity
        if interval is not None:
            params["interval"] = interval
        if start_ts is not None:
            params["start_ts"] = start_ts
        if end_ts is not None:
            params["end_ts"] = end_ts
        async with ApiClient() as client:
            return await client.gamma_get("/prices-history", params)

    @mcp.tool
    async def get_gamma_prices_history_batch(
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Fetch batch historical prices via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_post("/prices-history/batch", body)

    @mcp.tool
    async def get_gamma_open_interest(market: str | None = None) -> dict[str, Any]:
        """Fetch open interest via the trading API."""
        params = {"market": market} if market else None
        async with ApiClient() as client:
            return await client.gamma_get("/open-interest", params)

    @mcp.tool
    async def list_gamma_trades(
        market: str | None = None,
        user: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List Polymarket trades via the trading API."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if market:
            params["market"] = market
        if user:
            params["user"] = user
        async with ApiClient() as client:
            return await client.gamma_get("/trades", params)
