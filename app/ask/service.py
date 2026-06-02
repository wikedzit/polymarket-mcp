from typing import Any

from fastmcp import FastMCP
from fastmcp.tools.base import Tool

from app.ask.catalog import ASK_TOOL_NAME, SENSITIVE_TOOLS, build_tool_catalog, validate_arguments
from app.ask.choice import parse_choice
from app.ask.llm import AskRouterLLM
from app.ask.schemas import AskCandidate, AskResult, RouterCandidate
from app.ask.session import AskSession, SessionStore
from app.config import settings


class AskService:
    def __init__(self, mcp: FastMCP) -> None:
        self._mcp = mcp
        self._llm = AskRouterLLM()
        self._sessions = SessionStore(ttl_seconds=settings.ask_session_ttl_seconds)
        self._catalog_cache: str | None = None
        self._tools_by_name: dict[str, Tool] | None = None

    async def handle(self, query: str, session_id: str | None = None) -> AskResult:
        query = query.strip()
        if not query:
            session = self._resolve_session(session_id, "")
            return AskResult(
                status="error",
                session_id=session.session_id,
                message="Please provide a non-empty query.",
                original_query=session.original_query,
            )

        session = self._resolve_session(session_id, query)

        if session.pending_candidates:
            chosen = parse_choice(query, session.pending_candidates)
            if chosen is not None:
                return await self._execute_candidate(session, chosen)
            return AskResult(
                status="clarify",
                session_id=session.session_id,
                message=self._invalid_choice_message(session.pending_candidates),
                original_query=session.original_query,
                candidates=session.pending_candidates,
            )

        return await self._route_with_llm(session, query)

    def _resolve_session(self, session_id: str | None, query: str) -> AskSession:
        if session_id:
            existing = self._sessions.get(session_id)
            if existing:
                if not existing.original_query:
                    existing.original_query = query
                return existing
        return self._sessions.create(query)

    async def _route_with_llm(self, session: AskSession, query: str) -> AskResult:
        if not self._llm.configured:
            return AskResult(
                status="error",
                session_id=session.session_id,
                message=(
                    "Ask router is not configured. Set OPENAI_API_KEY in the MCP server environment."
                ),
                original_query=session.original_query,
            )

        catalog, tools_by_name = await self._get_catalog()
        decision = await self._llm.route(
            query,
            catalog,
            original_query=session.original_query,
        )

        if decision.status == "not_found":
            self._sessions.clear_pending(session)
            return AskResult(
                status="not_found",
                session_id=session.session_id,
                message=decision.message
                or "I couldn't find a tool that matches your request.",
                original_query=session.original_query,
            )

        valid = self._validate_router_candidates(decision.candidates, tools_by_name)
        if not valid:
            self._sessions.clear_pending(session)
            return AskResult(
                status="not_found",
                session_id=session.session_id,
                message=decision.message
                or "I couldn't find a tool that matches your request.",
                original_query=session.original_query,
            )

        ask_candidates = self._to_ask_candidates(valid, tools_by_name)

        if self._should_execute(decision.status, ask_candidates):
            return await self._execute_candidate(session, ask_candidates[0])

        session.pending_candidates = ask_candidates
        if not session.original_query:
            session.original_query = query
        self._sessions.save(session)

        message = decision.message or self._clarify_message(ask_candidates)
        return AskResult(
            status="clarify",
            session_id=session.session_id,
            message=message,
            original_query=session.original_query,
            candidates=ask_candidates,
        )

    def _should_execute(self, llm_status: str, candidates: list[AskCandidate]) -> bool:
        if len(candidates) != 1:
            return False
        candidate = candidates[0]
        if candidate.tool in SENSITIVE_TOOLS:
            return False
        if llm_status != "execute":
            return False
        return candidate.confidence >= settings.ask_execute_confidence

    async def _execute_candidate(
        self, session: AskSession, candidate: AskCandidate
    ) -> AskResult:
        _, tools_by_name = await self._get_catalog()
        tool = tools_by_name.get(candidate.tool)
        arguments = candidate.arguments
        if tool is not None:
            try:
                arguments = validate_arguments(tool, arguments, strict=True)
            except ValueError as exc:
                session.pending_candidates = [candidate]
                self._sessions.save(session)
                return AskResult(
                    status="clarify",
                    session_id=session.session_id,
                    message=(
                        f"`{candidate.tool}` still needs more details before it can run: {exc}"
                    ),
                    original_query=session.original_query,
                    candidates=[candidate],
                )

        tool_result = await self._mcp.call_tool(candidate.tool, arguments)
        inner = tool_result.structured_content or {}

        self._sessions.clear_pending(session)

        if isinstance(inner, dict) and inner.get("ok") is False:
            err = inner.get("error") or {}
            return AskResult(
                status="error",
                session_id=session.session_id,
                message=err.get("message", "The selected tool returned an error."),
                original_query=session.original_query,
                tool_name=candidate.tool,
                tool_arguments=arguments,
                tool_result=inner,
            )

        return AskResult(
            status="executed",
            session_id=session.session_id,
            message=f"Executed {candidate.tool}.",
            original_query=session.original_query,
            tool_name=candidate.tool,
            tool_arguments=arguments,
            tool_result=inner.get("data") if isinstance(inner, dict) else inner,
        )

    def _validate_router_candidates(
        self,
        candidates: list[RouterCandidate],
        tools_by_name: dict[str, Tool],
    ) -> list[RouterCandidate]:
        valid: list[RouterCandidate] = []
        for candidate in candidates:
            if candidate.confidence < settings.ask_clarify_confidence:
                continue
            tool = tools_by_name.get(candidate.tool)
            if tool is None:
                continue
            try:
                validate_arguments(tool, candidate.arguments, strict=False)
            except ValueError:
                continue
            valid.append(candidate)
        valid.sort(key=lambda c: c.confidence, reverse=True)
        return valid[:5]

    def _to_ask_candidates(
        self,
        candidates: list[RouterCandidate],
        tools_by_name: dict[str, Tool],
    ) -> list[AskCandidate]:
        ask_candidates: list[AskCandidate] = []
        for index, candidate in enumerate(candidates, start=1):
            tool = tools_by_name[candidate.tool]
            ask_candidates.append(
                AskCandidate(
                    index=index,
                    tool=candidate.tool,
                    description=(tool.description or candidate.tool).strip(),
                    arguments=candidate.arguments,
                    reason=candidate.reason,
                    confidence=candidate.confidence,
                )
            )
        return ask_candidates

    @staticmethod
    def _invalid_choice_message(candidates: list[AskCandidate]) -> str:
        return (
            "I didn't recognize that choice. "
            + AskService._clarify_message(candidates)
        )

    @staticmethod
    def _clarify_message(candidates: list[AskCandidate]) -> str:
        if len(candidates) == 1:
            c = candidates[0]
            return (
                f"Please confirm you want to run `{c.tool}` "
                f"(reply `1`, `yes`, or the tool name).\nReason: {c.reason or c.description}"
            )

        lines = [
            "I found multiple possible tools for your request.",
            "Reply with the option number or tool name:",
        ]
        for candidate in candidates:
            lines.append(
                f"{candidate.index}. {candidate.tool} — {candidate.reason or candidate.description}"
            )
        return "\n".join(lines)

    async def _get_catalog(self) -> tuple[str, dict[str, Tool]]:
        if self._catalog_cache is None or self._tools_by_name is None:
            self._catalog_cache, self._tools_by_name = await build_tool_catalog(self._mcp)
        return self._catalog_cache, self._tools_by_name
