from typing import Any, Literal

from pydantic import BaseModel, Field


class AskCandidate(BaseModel):
    index: int = Field(description="1-based option number shown to the user")
    tool: str
    description: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    reason: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class AskResult(BaseModel):
    status: Literal["executed", "clarify", "not_found", "error"]
    session_id: str
    message: str
    original_query: str
    tool_name: str | None = None
    tool_arguments: dict[str, Any] | None = None
    tool_result: Any | None = None
    candidates: list[AskCandidate] | None = None


class RouterCandidate(BaseModel):
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = ""


class RouterDecision(BaseModel):
    status: Literal["execute", "clarify", "not_found"]
    message: str
    candidates: list[RouterCandidate] = Field(default_factory=list)
