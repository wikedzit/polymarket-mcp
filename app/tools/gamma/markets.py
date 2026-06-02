from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def _market_params(
    *,
    limit: int = 10,
    offset: int = 0,
    active: bool = True,
    closed: bool = False,
    tag: str | None = None,
    tag_id: str | None = None,
    order: str | None = None,
    summarize: bool = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "limit": limit,
        "offset": offset,
        "active": active,
        "closed": closed,
        "summarize": summarize,
    }
    if tag:
        params["tag"] = tag
    if tag_id:
        params["tag_id"] = tag_id
    if order:
        params["order"] = order
    return params


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def list_gamma_markets(
        limit: int = 10,
        offset: int = 0,
        active: bool = True,
        closed: bool = False,
        tag: str | None = None,
        tag_id: str | None = None,
        order: str | None = None,
        summarize: bool = True,
    ) -> list[dict[str, Any]]:
        """List Polymarket markets via the trading API Gamma service."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/markets",
                _market_params(
                    limit=limit,
                    offset=offset,
                    active=active,
                    closed=closed,
                    tag=tag,
                    tag_id=tag_id,
                    order=order,
                    summarize=summarize,
                ),
            )

    @tool
    async def get_gamma_markets_by_condition_ids(
        condition_ids: list[str],
        summarize: bool = True,
    ) -> list[dict[str, Any]]:
        """Fetch Polymarket markets by condition IDs via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/markets",
                {"condition_ids": condition_ids, "summarize": summarize},
            )

    @tool
    async def list_gamma_markets_keyset(
        after_cursor: str | None = None,
        limit: int = 10,
        active: bool = True,
        closed: bool = False,
        tag_slug: str | None = None,
        summarize: bool = True,
    ) -> list[dict[str, Any]]:
        """List Polymarket markets using Gamma keyset pagination via the trading API."""
        params: dict[str, Any] = {
            "limit": limit,
            "active": active,
            "closed": closed,
            "summarize": summarize,
        }
        if after_cursor:
            params["after_cursor"] = after_cursor
        if tag_slug:
            params["tag_slug"] = tag_slug
        async with ApiClient() as client:
            return await client.gamma_get("/markets/keyset", params)

    @tool
    async def list_gamma_sampling_markets(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List Polymarket sampling markets via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/markets/sampling",
                {"limit": limit, "offset": offset},
            )

    @tool
    async def list_gamma_sampling_markets_simplified(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List simplified Polymarket sampling markets via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/markets/sampling-simplified",
                {"limit": limit, "offset": offset},
            )

    @tool
    async def list_gamma_markets_simplified(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List simplified Polymarket markets via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/markets/simplified",
                {"limit": limit, "offset": offset},
            )

    @tool
    async def get_gamma_market_by_slug(slug: str, summarize: bool = False) -> dict[str, Any]:
        """Fetch a Polymarket market by URL slug via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/markets/slug/{slug}", {"summarize": summarize})

    @tool
    async def get_gamma_market(market_id: str, summarize: bool = False) -> dict[str, Any]:
        """Fetch a Polymarket market by Gamma market ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/markets/{market_id}", {"summarize": summarize})

    @tool
    async def get_gamma_market_by_token(token_id: str, summarize: bool = False) -> dict[str, Any]:
        """Resolve a parent market from an outcome token ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                f"/markets/by-token/{token_id}",
                {"summarize": summarize},
            )

    @tool
    async def get_gamma_market_tags(market_id: str) -> list[dict[str, Any]]:
        """Fetch tags attached to a market via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/markets/{market_id}/tags")
