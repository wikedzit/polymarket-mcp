from typing import Any

from fastmcp import FastMCP

from app.clients.api import ApiClient
from app.tools.helpers import make_tool


def register(mcp: FastMCP) -> None:
    tool = make_tool(mcp)

    @tool
    async def create_paper_account(
        name: str,
        starting_balance_usdc: float | None = None,
    ) -> Any:
        """Create a simulated paper trading account with virtual USDC."""
        body: dict[str, Any] = {"name": name}
        if starting_balance_usdc is not None:
            body["starting_balance_usdc"] = starting_balance_usdc
        async with ApiClient() as client:
            return await client.paper_post("/accounts", json=body)

    @tool
    async def list_paper_accounts() -> Any:
        """List active paper trading accounts for the current API access token."""
        async with ApiClient() as client:
            return await client.paper_get("/accounts")

    @tool
    async def get_paper_account(account_id: str) -> Any:
        """Get a paper trading account summary by account ID."""
        async with ApiClient() as client:
            return await client.paper_get(f"/accounts/{account_id}")

    @tool
    async def get_paper_balance(account_id: str) -> Any:
        """Get virtual USDC balance for a paper account."""
        async with ApiClient() as client:
            return await client.paper_get(f"/accounts/{account_id}/balance")

    @tool
    async def get_paper_positions(account_id: str) -> Any:
        """Get open paper positions marked to live midpoints."""
        async with ApiClient() as client:
            return await client.paper_get(f"/accounts/{account_id}/positions")

    @tool
    async def get_paper_portfolio(account_id: str) -> Any:
        """Get paper portfolio value (cash + marked positions)."""
        async with ApiClient() as client:
            return await client.paper_get(f"/accounts/{account_id}/portfolio")

    @tool
    async def reset_paper_account(account_id: str) -> Any:
        """Full paper account reset: starting balance, cancel orders, clear positions."""
        async with ApiClient() as client:
            return await client.paper_post(f"/accounts/{account_id}/reset")

    @tool
    async def reset_paper_balance(
        account_id: str,
        balance_usdc: float | None = None,
        update_starting_balance: bool = False,
    ) -> Any:
        """Reset virtual USDC cash for a paper account. Keeps positions; cancels open orders."""
        body: dict[str, Any] = {"update_starting_balance": update_starting_balance}
        if balance_usdc is not None:
            body["balance_usdc"] = balance_usdc
        async with ApiClient() as client:
            return await client.paper_post(f"/accounts/{account_id}/balance/reset", json=body)
