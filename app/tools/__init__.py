from fastmcp import FastMCP

from app.tools.bridge import register as register_bridge
from app.tools.clob import register as register_clob
from app.tools.data import register as register_data
from app.tools.gamma import register as register_gamma
from app.tools.health import register as register_health


def register_tools(mcp: FastMCP) -> None:
    register_health(mcp)
    register_gamma(mcp)
    register_clob(mcp)
    register_data(mcp)
    register_bridge(mcp)
