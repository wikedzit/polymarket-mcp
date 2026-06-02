from typing import Any, Literal

from fastmcp import FastMCP

from app.clients.api import ApiClient
from app.clients.credentials import credentials_from_kwargs
from app.tools.helpers import make_tool


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def post_clob_order(
        body: dict[str, Any],
        private_key: str | None = None,
        deposit_wallet_address: str | None = None,
        poly_api_key: str | None = None,
        poly_api_secret: str | None = None,
        poly_passphrase: str | None = None,
        poly_builder_code: str | None = None,
        clob_signature_type: int | None = None,
    ) -> Any:
        """Post a pre-signed CLOB order payload (advanced). Prefer post_clob_market_order."""
        creds = credentials_from_kwargs(
            private_key=private_key,
            deposit_wallet_address=deposit_wallet_address,
            poly_api_key=poly_api_key,
            poly_api_secret=poly_api_secret,
            poly_passphrase=poly_passphrase,
            poly_builder_code=poly_builder_code,
            clob_signature_type=clob_signature_type,
        )
        async with ApiClient(credentials=creds) as client:
            return await client.clob_post("/order", body)

    @tool
    async def post_clob_market_order(
        token_id: str,
        amount: float,
        side: str = "BUY",
        order_type: str = "FOK",
        tick_size: str = "0.01",
        neg_risk: bool = False,
        mode: Literal["real", "paper"] = "real",
        paper_account_id: str | None = None,
        private_key: str | None = None,
        deposit_wallet_address: str | None = None,
        poly_api_key: str | None = None,
        poly_api_secret: str | None = None,
        poly_passphrase: str | None = None,
        poly_builder_code: str | None = None,
        clob_signature_type: int | None = None,
    ) -> Any:
        """Create and post a market order. Set mode=paper for simulated trading."""
        body: dict[str, Any] = {
            "token_id": token_id,
            "amount": amount,
            "side": side,
            "order_type": order_type,
            "tick_size": tick_size,
            "neg_risk": neg_risk,
            "mode": mode,
        }
        if paper_account_id:
            body["paper_account_id"] = paper_account_id
        params = {"mode": mode}
        creds = credentials_from_kwargs(
            private_key=private_key,
            deposit_wallet_address=deposit_wallet_address,
            poly_api_key=poly_api_key,
            poly_api_secret=poly_api_secret,
            poly_passphrase=poly_passphrase,
            poly_builder_code=poly_builder_code,
            clob_signature_type=clob_signature_type,
        )
        async with ApiClient(credentials=creds) as client:
            return await client.clob_post("/order/market", body, params=params)

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
        mode: Literal["real", "paper"] = "real",
        paper_account_id: str | None = None,
        private_key: str | None = None,
        deposit_wallet_address: str | None = None,
        poly_api_key: str | None = None,
        poly_api_secret: str | None = None,
        poly_passphrase: str | None = None,
        poly_builder_code: str | None = None,
        clob_signature_type: int | None = None,
    ) -> Any:
        """Create and post a limit order. Set mode=paper for simulated trading."""
        body: dict[str, Any] = {
            "token_id": token_id,
            "price": price,
            "size": size,
            "side": side,
            "order_type": order_type,
            "tick_size": tick_size,
            "neg_risk": neg_risk,
            "post_only": post_only,
            "mode": mode,
        }
        if paper_account_id:
            body["paper_account_id"] = paper_account_id
        params = {"mode": mode}
        creds = credentials_from_kwargs(
            private_key=private_key,
            deposit_wallet_address=deposit_wallet_address,
            poly_api_key=poly_api_key,
            poly_api_secret=poly_api_secret,
            poly_passphrase=poly_passphrase,
            poly_builder_code=poly_builder_code,
            clob_signature_type=clob_signature_type,
        )
        async with ApiClient(credentials=creds) as client:
            return await client.clob_post("/order/limit", body, params=params)

    @tool
    async def get_clob_open_orders(
        market: str | None = None,
        asset_id: str | None = None,
        mode: Literal["real", "paper"] = "real",
        paper_account_id: str | None = None,
        status: str | None = None,
    ) -> Any:
        """Get orders via the trading API. Pass mode=paper or mode=real."""
        params: dict[str, Any] = {"mode": mode}
        if market:
            params["market"] = market
        if asset_id:
            params["asset_id"] = asset_id
        if paper_account_id:
            params["paper_account_id"] = paper_account_id
        if status:
            params["status"] = status
        async with ApiClient() as client:
            return await client.clob_get("/data/orders", params)

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
    async def cancel_all_clob_orders(
        mode: Literal["real", "paper"] = "real",
        paper_account_id: str | None = None,
    ) -> Any:
        """Cancel all orders. Pass mode=paper for simulated orders."""
        params: dict[str, Any] = {"mode": mode}
        if paper_account_id:
            params["paper_account_id"] = paper_account_id
        async with ApiClient() as client:
            return await client.clob_delete("/cancel-all", params=params)

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
        private_key: str | None = None,
        deposit_wallet_address: str | None = None,
        poly_api_key: str | None = None,
        poly_api_secret: str | None = None,
        poly_passphrase: str | None = None,
        poly_builder_code: str | None = None,
        clob_signature_type: int | None = None,
    ) -> Any:
        """Get CLOB balance and allowance via the trading API."""
        params: dict[str, Any] = {"asset_type": asset_type}
        if token_id:
            params["token_id"] = token_id
        creds = credentials_from_kwargs(
            private_key=private_key,
            deposit_wallet_address=deposit_wallet_address,
            poly_api_key=poly_api_key,
            poly_api_secret=poly_api_secret,
            poly_passphrase=poly_passphrase,
            poly_builder_code=poly_builder_code,
            clob_signature_type=clob_signature_type,
        )
        async with ApiClient(credentials=creds) as client:
            return await client.clob_get("/balance-allowance", params)

    @tool
    async def derive_clob_api_key(
        nonce: int | None = None,
        private_key: str | None = None,
        deposit_wallet_address: str | None = None,
    ) -> Any:
        """Derive CLOB L2 API credentials via the trading API (requires PRIVATE_KEY)."""
        params = {"nonce": nonce} if nonce is not None else None
        creds = credentials_from_kwargs(
            private_key=private_key,
            deposit_wallet_address=deposit_wallet_address,
        )
        async with ApiClient(credentials=creds) as client:
            return await client.clob_get("/auth/derive-api-key", params)
