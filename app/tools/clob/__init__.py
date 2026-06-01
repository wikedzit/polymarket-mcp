from fastmcp import FastMCP

from app.tools.clob import account, history, market_data, markets, trading


def register(mcp: FastMCP) -> None:
    for module in (market_data, markets, history, trading, account):
        module.register(mcp)
