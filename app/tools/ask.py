from typing import Any

from fastmcp import FastMCP

from app.ask.service import AskService
from app.tools.helpers import make_tool

_service: AskService | None = None


def register(mcp: FastMCP) -> None:
    global _service
    _service = AskService(mcp)
    tool = make_tool(mcp)

    @tool
    async def ask(query: str, session_id: str | None = None) -> dict[str, Any]:
        """Route natural language to the best Polymarket MCP tool and execute it.

        Pass only text in `query`. On ambiguous matches, returns numbered options —
        reply with the option number or tool name using the same `session_id` to
        execute without re-running the LLM.
        """
        assert _service is not None
        result = await _service.handle(query, session_id)
        return result.model_dump()
