from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar

import httpx
from fastmcp import FastMCP

from app.clients.errors import ApiClientError
from app.schemas.responses import ToolResponse

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])

_TOOL_OUTPUT_SCHEMA = ToolResponse.model_json_schema()


async def execute(fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> ToolResponse:
    """Run a tool function and return a structured ToolResponse."""
    try:
        data = await fn(*args, **kwargs)
        return ToolResponse.success(data)
    except ApiClientError as exc:
        return ToolResponse.from_api_error(exc)
    except httpx.TimeoutException:
        return ToolResponse.failure("timeout", "Request to the trading API timed out")
    except httpx.RequestError as exc:
        return ToolResponse.failure(
            "connection_error",
            "Could not reach the trading API",
            detail=str(exc),
        )
    except Exception as exc:
        return ToolResponse.failure("internal_error", str(exc))


def make_tool(mcp: FastMCP) -> Callable[[F], F]:
    """Register a tool that always returns a structured ToolResponse envelope."""

    def decorator(fn: F) -> F:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> ToolResponse:
            return await execute(fn, *args, **kwargs)

        mcp.tool(output_schema=_TOOL_OUTPUT_SCHEMA)(wrapper)
        return fn

    return decorator
