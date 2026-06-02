from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def get_gamma_prices_history(
        market: str,
        fidelity: int | None = None,
        interval: str | None = None,
        start_ts: int | None = None,
        end_ts: int | None = None,
    ) -> dict[str, Any]:
        """Fetch historical prices from Gamma via the trading API."""
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

    @tool
    async def get_gamma_prices_history_batch(body: dict[str, Any]) -> dict[str, Any]:
        """Fetch batch Gamma price history via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_post("/prices-history/batch", body)
