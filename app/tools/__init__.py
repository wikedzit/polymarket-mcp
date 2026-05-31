from fastmcp import FastMCP

from app.tools import api_health, markets, orderbook


def register_tools(mcp: FastMCP) -> None:
    api_health.register(mcp)
    markets.register(mcp)
    orderbook.register(mcp)
