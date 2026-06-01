from fastmcp import FastMCP

from app.tools.data import core, leaderboards, markets


def register(mcp: FastMCP) -> None:
    for module in (core, markets, leaderboards):
        module.register(mcp)
