from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def get_clob_prices_history(
        market: str,
        interval: str | None = None,
        fidelity: int | None = None,
        start_ts: int | None = None,
        end_ts: int | None = None,
    ) -> Any:
        """Get CLOB price history via the trading API."""
        params: dict[str, Any] = {"market": market}
        if interval:
            params["interval"] = interval
        if fidelity is not None:
            params["fidelity"] = fidelity
        if start_ts is not None:
            params["startTs"] = start_ts
        if end_ts is not None:
            params["endTs"] = end_ts
        async with ApiClient() as client:
            return await client.clob_get("/prices-history", params)

    @tool
    async def get_clob_batch_prices_history(body: dict[str, Any]) -> Any:
        """Get batch CLOB price history via the trading API."""
        async with ApiClient() as client:
            return await client.clob_post("/batch-prices-history", body)
