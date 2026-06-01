from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def get_bridge_supported_assets() -> dict[str, Any]:
        """Get supported bridge chains and tokens via the trading API."""
        async with ApiClient() as client:
            return await client.bridge_get("/supported-assets")

    @mcp.tool
    async def post_bridge_quote(
        from_amount_base_unit: str,
        from_chain_id: str,
        from_token_address: str,
        recipient_address: str,
        to_chain_id: str,
        to_token_address: str,
    ) -> dict[str, Any]:
        """Preview bridge fees and estimated output via the trading API."""
        body = {
            "fromAmountBaseUnit": from_amount_base_unit,
            "fromChainId": from_chain_id,
            "fromTokenAddress": from_token_address,
            "recipientAddress": recipient_address,
            "toChainId": to_chain_id,
            "toTokenAddress": to_token_address,
        }
        async with ApiClient() as client:
            return await client.bridge_post("/quote", body)

    @mcp.tool
    async def post_bridge_deposit(address: str) -> dict[str, Any]:
        """Create multi-chain deposit addresses for a Polymarket wallet via the trading API."""
        async with ApiClient() as client:
            return await client.bridge_post("/deposit", {"address": address})

    @mcp.tool
    async def post_bridge_withdraw(
        address: str,
        to_chain_id: str,
        to_token_address: str,
        recipient_addr: str,
    ) -> dict[str, Any]:
        """Create withdrawal addresses for bridging pUSD off Polymarket via the trading API."""
        body = {
            "address": address,
            "toChainId": to_chain_id,
            "toTokenAddress": to_token_address,
            "recipientAddr": recipient_addr,
        }
        async with ApiClient() as client:
            return await client.bridge_post("/withdraw", body)

    @mcp.tool
    async def get_bridge_status(address: str) -> dict[str, Any]:
        """Track bridge deposit or withdrawal progress via the trading API."""
        async with ApiClient() as client:
            return await client.bridge_get(f"/status/{address}")
