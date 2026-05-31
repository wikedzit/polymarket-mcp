from fastmcp import FastMCP

from app.tools.gamma import events, history, markets, profiles, search, series, sports, tags


def register(mcp: FastMCP) -> None:
    for module in (
        markets,
        events,
        search,
        tags,
        series,
        sports,
        profiles,
        history,
    ):
        module.register(mcp)
