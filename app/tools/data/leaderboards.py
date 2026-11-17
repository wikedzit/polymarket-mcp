from typing import Any, Literal

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def _validate_limit_offset(limit: int, offset: int) -> None:
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50 inclusive")
    if offset < 0:
        raise ValueError("offset must be greater than or equal to 0")


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def get_data_leaderboard(
        category: Literal[
            "OVERALL",
            "POLITICS",
            "SPORTS",
            "CRYPTO",
            "CULTURE",
            "MENTIONS",
            "WEATHER",
            "ECONOMICS",
            "TECH",
            "FINANCE",
        ] = "OVERALL",
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get trader leaderboard via the trading API Data service."""
        _validate_limit_offset(limit, offset)
        async with ApiClient() as client:
            return await client.data_get(
                "/v1/leaderboard",
                {"category": category, "limit": limit, "offset": offset},
            )

    @tool
    async def get_data_builder_leaderboard(
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get builder leaderboard via the trading API."""
        _validate_limit_offset(limit, offset)
        async with ApiClient() as client:
            return await client.data_get(
                "/v1/builders/leaderboard",
                {"limit": limit, "offset": offset},
            )

    @tool
    async def get_data_builder_volume(
        builder: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """Get builder volume time series via the trading API."""
        params: dict[str, Any] = {}
        if builder:
            params["builder"] = builder
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        async with ApiClient() as client:
            return await client.data_get("/v1/builders/volume", params or None)
