from typing import Any, Literal

import httpx

from app.config import settings


class ApiClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = (base_url or settings.polymarket_api_url).rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=30.0)

    async def __aenter__(self) -> "ApiClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    async def _get_json(self, path: str, **kwargs: Any) -> Any:
        response = await self._client.get(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def health(self) -> dict[str, str]:
        return await self._get_json("/health/")

    async def list_active_events(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        return await self._get_json(
            "/markets/events",
            params={"limit": limit, "offset": offset},
        )

    async def get_market_by_slug(self, slug: str) -> dict[str, Any]:
        return await self._get_json(f"/markets/slug/{slug}")

    async def list_active_markets(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        return await self._get_json(
            "/markets/",
            params={"limit": limit, "offset": offset},
        )

    async def get_markets_by_condition_ids(
        self,
        condition_ids: list[str],
    ) -> list[dict[str, Any]]:
        return await self._get_json(
            "/markets/",
            params={"condition_ids": condition_ids},
        )

    async def clob_server_time(self) -> dict[str, int]:
        return await self._get_json("/clob/time")

    async def get_orderbook(self, token_id: str) -> dict[str, Any]:
        return await self._get_json(
            "/clob/orderbook",
            params={"token_id": token_id},
        )

    async def get_midpoint(self, token_id: str) -> dict[str, str]:
        return await self._get_json(
            "/clob/midpoint",
            params={"token_id": token_id},
        )

    async def get_spread(self, token_id: str) -> dict[str, str]:
        return await self._get_json(
            "/clob/spread",
            params={"token_id": token_id},
        )

    async def get_price(
        self,
        token_id: str,
        side: Literal["BUY", "SELL"],
    ) -> dict[str, str]:
        return await self._get_json(
            "/clob/price",
            params={"token_id": token_id, "side": side},
        )

    async def get_tick_size(self, token_id: str) -> dict[str, str]:
        return await self._get_json(
            "/clob/tick-size",
            params={"token_id": token_id},
        )
