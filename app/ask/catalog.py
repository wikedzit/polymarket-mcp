from typing import Any

from fastmcp import FastMCP
from fastmcp.tools.base import Tool

ASK_TOOL_NAME = "ask"

SENSITIVE_TOOLS = frozenset(
    {
        "post_clob_order",
        "post_clob_market_order",
        "post_clob_limit_order",
        "cancel_clob_order",
        "cancel_all_clob_orders",
        "post_clob_heartbeat",
        "derive_clob_api_key",
        "post_bridge_deposit",
        "post_bridge_withdraw",
        "post_bridge_quote",
    }
)


async def build_tool_catalog(mcp: FastMCP) -> tuple[str, dict[str, Tool]]:
    tools = await mcp.list_tools()
    by_name: dict[str, Tool] = {}
    lines: list[str] = []
    for tool in sorted(tools, key=lambda t: t.name):
        if tool.name == ASK_TOOL_NAME:
            continue
        by_name[tool.name] = tool
        desc = (tool.description or "").replace("\n", " ").strip()
        lines.append(f"- {tool.name}: {desc}")
    return "\n".join(lines), by_name


def _coerce_value(value: Any, prop: dict[str, Any]) -> Any:
    """Coerce common LLM/client mismatches (e.g. numeric series_id) to schema types."""
    if value is None:
        return value

    prop_type = prop.get("type")
    if prop_type == "string" and isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    if prop_type == "integer" and isinstance(value, str) and value.isdigit():
        return int(value)

    if prop_type == "number" and isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return value

    return value


def validate_arguments(
    tool: Tool,
    arguments: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Keep only parameters declared on the tool schema."""
    properties = tool.parameters.get("properties", {})
    cleaned: dict[str, Any] = {}
    for key, value in arguments.items():
        if key not in properties:
            continue
        cleaned[key] = _coerce_value(value, properties[key])

    if not strict:
        return cleaned

    required = tool.parameters.get("required", [])
    for key in required:
        if key not in cleaned:
            raise ValueError(f"Missing required argument '{key}' for tool '{tool.name}'")
    return cleaned
