from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def get_gamma_profile(address: str) -> dict[str, Any]:
        """Fetch a Polymarket user profile via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/profiles/{address}")

    @mcp.tool
    async def list_gamma_comments(
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List Polymarket comments via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get("/comments", {"limit": limit, "offset": offset})

    @mcp.tool
    async def list_gamma_comments_by_user(
        address: str,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List Polymarket comments for a user address via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(
                f"/comments/by-user/{address}",
                {"limit": limit, "offset": offset},
            )

    @mcp.tool
    async def get_gamma_comment(comment_id: str) -> dict[str, Any]:
        """Fetch a Polymarket comment by ID via the trading API."""
        async with ApiClient() as client:
            return await client.gamma_get(f"/comments/{comment_id}")
