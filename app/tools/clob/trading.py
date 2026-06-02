from typing import Any

from fastmcp import FastMCP
from app.tools.helpers import make_tool

from app.clients.api import ApiClient


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def post_clob_order(body: dict[str, Any]) -> Any:
        """Post a pre-signed CLOB order payload (advanced). Prefer post_clob_market_order."""
        async with ApiClient() as client:
            return await client.clob_post("/order", body)

    @tool
    async def post_clob_market_order(
        token_id: str,
        amount: float,
        side: str = "BUY",
        order_type: str = "FOK",
        tick_size: str = "0.01",
        neg_risk: bool = False,
    ) -> Any:
        """Create, sign, and post a market order (FOK/FAK) via the trading API."""
        body = {
            "token_id": token_id,
            "amount": amount,
            "side": side,
            "order_type": order_type,
            "tick_size": tick_size,
            "neg_risk": neg_risk,
        }
        async with ApiClient() as client:
            return await client.clob_post("/order/market", body)

    @tool
    async def post_clob_limit_order(
        token_id: str,
        price: float,
        size: float,
        side: str = "BUY",
        order_type: str = "GTC",
        tick_size: str = "0.01",
        neg_risk: bool = False,
        post_only: bool = False,
    ) -> Any:
        """Create, sign, and post a limit order via the trading API."""
        body = {
            "token_id": token_id,
            "price": price,
            "size": size,
            "side": side,
            "order_type": order_type,
            "tick_size": tick_size,
            "neg_risk": neg_risk,
            "post_only": post_only,
        }
        async with ApiClient() as client:
            return await client.clob_post("/order/limit", body)

    @tool
    async def get_clob_open_orders(
        market: str | None = None,
        asset_id: str | None = None,
    ) -> Any:
        """Get open CLOB orders via the trading API."""
        params: dict[str, Any] = {}
        if market:
            params["market"] = market
        if asset_id:
            params["asset_id"] = asset_id
        async with ApiClient() as client:
            return await client.clob_get("/data/orders", params or None)

    @tool
    async def get_clob_order(order_id: str) -> Any:
        """Get a CLOB order by ID via the trading API."""
        async with ApiClient() as client:
            return await client.clob_get(f"/data/order/{order_id}")

    @tool
    async def cancel_clob_order(order_id: str) -> Any:
        """Cancel a CLOB order via the trading API."""
        async with ApiClient() as client:
            return await client.clob_delete(f"/order/{order_id}")

    @tool
    async def cancel_all_clob_orders() -> Any:
        """Cancel all CLOB orders via the trading API."""
        async with ApiClient() as client:
            return await client.clob_delete("/cancel-all")

    @tool
    async def post_clob_heartbeat(heartbeat_id: str = "") -> Any:
        """Send CLOB heartbeat via the trading API (keeps resting orders alive)."""
        async with ApiClient() as client:
            return await client.clob_post("/v1/heartbeats", {"heartbeat_id": heartbeat_id})

    @tool
    async def get_clob_trades(
        market: str | None = None,
        asset_id: str | None = None,
    ) -> Any:
        """Get authenticated CLOB trades via the trading API."""
        params: dict[str, Any] = {}
        if market:
            params["market"] = market
        if asset_id:
            params["asset_id"] = asset_id
        async with ApiClient() as client:
            return await client.clob_get("/data/trades", params or None)

    @tool
    async def get_clob_balance_allowance(
        asset_type: str = "COLLATERAL",
        token_id: str | None = None,
    ) -> Any:
        """Get CLOB balance and allowance via the trading API."""
        params: dict[str, Any] = {"asset_type": asset_type}
        if token_id:
            params["token_id"] = token_id
        async with ApiClient() as client:
            return await client.clob_get("/balance-allowance", params)

    @tool
    async def derive_clob_api_key(nonce: int | None = None) -> Any:
        """Derive CLOB L2 API credentials via the trading API (requires PRIVATE_KEY)."""
        params = {"nonce": nonce} if nonce is not None else None
        async with ApiClient() as client:
            return await client.clob_get("/auth/derive-api-key", params)
