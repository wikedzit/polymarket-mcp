from fastmcp import FastMCP

from app.tools import register_tools

mcp = FastMCP(
    "Polymarket MCP",
    instructions=(
        "MCP server for Polymarket trading operations. "
        "All tools proxy requests to the local Polymarket trading API."
    ),
    version="0.1.0",
)

register_tools(mcp)


if __name__ == "__main__":
    mcp.run()
