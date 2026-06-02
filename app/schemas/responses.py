from typing import Any

from pydantic import BaseModel, Field

from app.clients.errors import ApiClientError


class ToolErrorDetail(BaseModel):
    code: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable error message")
    status_code: int | None = Field(default=None, description="HTTP status from upstream API")
    path: str | None = Field(default=None, description="Upstream API path")
    detail: Any | None = Field(default=None, description="Additional error context from upstream")


class ToolResponse(BaseModel):
    """Standard envelope for every MCP tool result."""

    ok: bool = Field(description="True when the tool completed successfully")
    data: Any | None = Field(default=None, description="Tool payload on success")
    error: ToolErrorDetail | None = Field(default=None, description="Error details on failure")

    @classmethod
    def success(cls, data: Any) -> "ToolResponse":
        return cls(ok=True, data=data)

    @classmethod
    def failure(
        cls,
        code: str,
        message: str,
        *,
        status_code: int | None = None,
        path: str | None = None,
        detail: Any = None,
    ) -> "ToolResponse":
        return cls(
            ok=False,
            error=ToolErrorDetail(
                code=code,
                message=message,
                status_code=status_code,
                path=path,
                detail=detail,
            ),
        )

    @classmethod
    def from_api_error(cls, exc: ApiClientError) -> "ToolResponse":
        return cls.failure(
            exc.code,
            exc.message,
            status_code=exc.status_code,
            path=exc.path,
            detail=exc.detail,
        )
