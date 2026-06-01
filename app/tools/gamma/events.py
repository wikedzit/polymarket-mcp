from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def list_gamma_events(
        limit: int = 10,
        offset: int = 0,
        active: bool = True,
        closed: bool = False,
        tag: str | None = None,
        tag_id: str | None = None,
        order: str | None = None,
        summarize: bool = True,
    ) -> list[dict[str, Any]]:
        """List active Polymarket events via the trading API Gamma service."""
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
        async with ApiClient() as client:
            return await client.gamma_get("/events", params)

    @mcp.tool
    async def list_gamma_events_keyset(
        after_cursor: str | None = None,
        limit: int = 10,
        active: bool = True,
        closed: bool = False,
        tag_slug: str | None = None,
        summarize: bool = True,
    ) -> list[dict[str, Any]]:
        """List Polymarket events using Gamma keyset pagination via the trading API."""
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
            return await client.gamma_get("/events/keyset", params)

    @mcp.tool
    async def list_gamma_event_tags(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List Polymarket event tags via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                "/events/tags",
                {"limit": limit, "offset": offset},
            )

    @mcp.tool
    async def get_gamma_event(event_id: str, summarize: bool = False) -> dict[str, Any]:
        """Fetch a Polymarket event by ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/events/{event_id}", {"summarize": summarize})

    @mcp.tool
    async def get_gamma_event_by_slug(slug: str, summarize: bool = False) -> dict[str, Any]:
        """Fetch a Polymarket event by slug via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/events/slug/{slug}", {"summarize": summarize})

    @mcp.tool
    async def get_gamma_event_live_volume(event_id: str) -> dict[str, Any]:
        """Fetch live volume for an event via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/events/{event_id}/volume/live")
