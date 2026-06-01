from fastmcp import FastMCP

from app.tools.bridge import core


def register(mcp: FastMCP) -> None:
    for module in (core,):
        module.register(mcp)
