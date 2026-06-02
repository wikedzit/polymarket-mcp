import json
import re

from fastmcp.server.middleware import Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams

from fastmcp.tools.base import ToolResult
from mcp.types import TextContent

from app.schemas.responses import ToolResponse

_ERROR_PREFIX = re.compile(r"^Error calling tool '[^']+': ")


class StructuredResponseMiddleware(Middleware):
    """Normalize legacy tool outputs into the standard ToolResponse envelope."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next,
    ) -> ToolResult:
        result: ToolResult = await call_next(context)

        if isinstance(result.structured_content, dict) and "ok" in result.structured_content:
            return result

        if result.structured_content is not None:
            data = self._unwrap_data(result.structured_content)
            if data is not None:
                return self._success_result(data)

        if result.content:
            text = self._first_text(result)
            if text:
                if text.startswith("Error calling tool"):
                    message = _ERROR_PREFIX.sub("", text)
                    return self._failure_result("tool_error", message)
                if text.startswith("Output validation error:"):
                    return self._failure_result("output_validation_error", text)

        return result

    @staticmethod
    def _unwrap_data(structured: dict) -> Any | None:
        if set(structured.keys()) == {"result"}:
            return structured["result"]
        return structured

    @staticmethod
    def _first_text(result: ToolResult) -> str | None:
        for block in result.content:
            if isinstance(block, TextContent):
                return block.text
            if getattr(block, "type", None) == "text":
                return getattr(block, "text", None)
        return None

    def _success_result(self, data: Any) -> ToolResult:
        envelope = ToolResponse.success(data).model_dump()
        return ToolResult(
            content=[TextContent(type="text", text=json.dumps(envelope))],
            structured_content=envelope,
        )

    def _failure_result(self, code: str, message: str) -> ToolResult:
        envelope = ToolResponse.failure(code, message).model_dump()
        return ToolResult(
            content=[TextContent(type="text", text=json.dumps(envelope))],
            structured_content=envelope,
        )
