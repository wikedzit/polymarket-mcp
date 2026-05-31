from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def list_gamma_tags(limit: int = 10, offset: int = 0) -> list[dict[str, Any]]:
        """List Polymarket tags via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get("/tags", {"limit": limit, "offset": offset})

    @mcp.tool
    async def get_gamma_tag(tag_id: str) -> dict[str, Any]:
        """Fetch a Polymarket tag by ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/tags/{tag_id}")

    @mcp.tool
    async def get_gamma_tag_by_slug(slug: str) -> dict[str, Any]:
        """Fetch a Polymarket tag by slug via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/tags/slug/{slug}")

    @mcp.tool
    async def get_gamma_related_tags_by_id(tag_id: str) -> list[dict[str, Any]]:
        """Fetch related Polymarket tags by tag ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/tags/{tag_id}/related")

    @mcp.tool
    async def get_gamma_related_tags_by_slug(slug: str) -> list[dict[str, Any]]:
        """Fetch related Polymarket tags by tag slug via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/tags/slug/{slug}/related")
