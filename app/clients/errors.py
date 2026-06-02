from typing import Any


class ApiClientError(Exception):
    """Structured error from the Polymarket trading API."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "api_error",
        status_code: int | None = None,
        path: str | None = None,
        detail: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.path = path
        self.detail = detail
