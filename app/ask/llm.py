from typing import Any

import httpx

from app.ask.schemas import RouterDecision
from app.config import settings

SYSTEM_PROMPT = """You are a routing assistant for a Polymarket MCP server.
Given a user query and a catalog of available tools, choose the best tool(s).

Respond with JSON only, matching this shape:
{
  "status": "execute" | "clarify" | "not_found",
  "message": "user-facing explanation",
  "candidates": [
    {"tool": "exact_tool_name", "arguments": {}, "confidence": 0.0-1.0, "reason": "why"}
  ]
}

Rules:
- status=execute ONLY when exactly one tool clearly matches (confidence >= 0.75).
- status=clarify when multiple tools could match OR confidence is moderate (0.4-0.74).
- status=not_found when no tool reasonably matches the request.
- candidates must use exact tool names from the catalog.
- Provide realistic arguments; use {} when no args needed.
- Never invent tool names.
- For balance queries use get_clob_balance_allowance with {"asset_type": "COLLATERAL"}.
- For BTC Up or Down 5m closed events use list_gamma_events with series_id "10684".
- String ID fields (series_id, token_id, event_id, etc.) must be JSON strings, not numbers.

Paper / simulated / demo / virtual trading:
- Keywords paper, demo, simulated, virtual, practice, fake money → paper trading mode.
- For paper orders use post_clob_market_order or post_clob_limit_order with
  {"mode": "paper", "paper_account_id": "<uuid>", ...}. Default mode is "real".
- Paper balance/portfolio: get_paper_balance, get_paper_portfolio, get_paper_positions
  (NOT get_clob_balance_allowance).
- Create paper accounts with create_paper_account. List with list_paper_accounts.
- Reset all paper state (balance + positions + orders): reset_paper_account.
- Reset only virtual USDC cash (keeps positions): reset_paper_balance.
- Paper accounts are scoped to the caller API access token; always pass paper_account_id.
- List paper orders: get_clob_open_orders with {"mode": "paper", "paper_account_id": "<uuid>"}.
- If user wants paper trading but no account_id, clarify or suggest create_paper_account /
  list_paper_accounts first.

- Trading/order intent (buy, sell, place order) is in scope even when details are missing:
  use status=clarify with the best matching order tool and partial arguments; explain what
  is still needed (token_id, price, size/amount, and paper_account_id when mode=paper).
  Do NOT use not_found for trading intent.
- When the user clearly wants paper/demo trading, include "mode": "paper" in order tool args.
- Trading/order tools should never use status=execute unless the user supplied all required
  fields explicitly (for paper orders: mode, paper_account_id, token_id, and amount or price/size)."""


class AskRouterLLM:
    def __init__(self) -> None:
        self._model = settings.openai_model
        self._base_url = settings.openai_base_url

    @property
    def configured(self) -> bool:
        return bool(settings.openai_api_key)

    async def route(
        self,
        query: str,
        catalog: str,
        *,
        original_query: str | None = None,
        pending_context: str | None = None,
    ) -> RouterDecision:
        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. Set it in the MCP server environment."
            )

        user_parts = [f"Tool catalog:\n{catalog}", f"\nUser query:\n{query}"]
        if original_query and original_query != query:
            user_parts.append(f"\nOriginal request:\n{original_query}")
        if pending_context:
            user_parts.append(f"\nContext:\n{pending_context}")

        schema = RouterDecision.model_json_schema()

        payload: dict[str, Any] = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "".join(user_parts)},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            body = response.json()

        content = body["choices"][0]["message"]["content"]
        return RouterDecision.model_validate_json(content)
