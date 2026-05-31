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

    async def _post_json(self, path: str, **kwargs: Any) -> Any:
        response = await self._client.post(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def health(self) -> dict[str, str]:
        return await self._get_json("/health/")

    async def gamma_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._get_json(f"/gamma{path}", params=params)

    async def gamma_post(self, path: str, json: dict[str, Any]) -> Any:
        return await self._post_json(f"/gamma{path}", json=json)

    async def list_gamma_markets(
        self,
        limit: int = 10,
        offset: int = 0,
        condition_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if condition_ids:
            params["condition_ids"] = condition_ids
        return await self.gamma_get("/markets", params)

    async def get_gamma_market_by_slug(self, slug: str) -> dict[str, Any]:
        return await self.gamma_get(f"/markets/slug/{slug}")

    async def get_gamma_market(self, market_id: str) -> dict[str, Any]:
        return await self.gamma_get(f"/markets/{market_id}")

    async def get_gamma_market_by_token(self, token_id: str) -> dict[str, Any]:
        return await self.gamma_get(f"/markets/by-token/{token_id}")

    async def list_gamma_events(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        return await self.gamma_get("/events", {"limit": limit, "offset": offset})

    async def get_gamma_event(self, event_id: str) -> dict[str, Any]:
        return await self.gamma_get(f"/events/{event_id}")

    async def get_gamma_event_by_slug(self, slug: str) -> dict[str, Any]:
        return await self.gamma_get(f"/events/slug/{slug}")

    async def gamma_search(
        self,
        q: str,
        search_type: Literal["markets", "events", "profiles"] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"q": q, "limit": limit}
        if search_type:
            params["type"] = search_type
        return await self.gamma_get("/search", params)

    async def clob_server_time(self) -> dict[str, int]:
        return await self._get_json("/clob/time")

    async def get_orderbook(self, token_id: str) -> dict[str, Any]:
        return await self._get_json("/clob/orderbook", params={"token_id": token_id})

    async def get_midpoint(self, token_id: str) -> dict[str, str]:
        return await self._get_json("/clob/midpoint", params={"token_id": token_id})

    async def get_spread(self, token_id: str) -> dict[str, str]:
        return await self._get_json("/clob/spread", params={"token_id": token_id})

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
        return await self._get_json("/clob/tick-size", params={"token_id": token_id})
