import json
from typing import Any, Literal

import httpx

from app.config import settings


class ApiClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = (base_url or settings.polymarket_api_url).rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=60.0)

    async def __aenter__(self) -> "ApiClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    async def _get_json(self, path: str, **kwargs: Any) -> Any:
        response = await self._client.get(path, **kwargs)
        response.raise_for_status()
        if not response.content:
            return None
        return response.json()

    async def _post_json(self, path: str, **kwargs: Any) -> Any:
        response = await self._client.post(path, **kwargs)
        response.raise_for_status()
        if not response.content:
            return None
        return response.json()

    async def _delete_json(self, path: str, **kwargs: Any) -> Any:
        response = await self._client.delete(path, **kwargs)
        response.raise_for_status()
        if not response.content:
            return None
        return response.json()

    async def health(self) -> dict[str, str]:
        return await self._get_json("/health/")

    async def gamma_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._get_json(f"/gamma{path}", params=params)

    async def gamma_post(self, path: str, json: dict[str, Any]) -> Any:
        return await self._post_json(f"/gamma{path}", json=json)

    async def data_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._get_json(f"/data{path}", params=params)

    async def bridge_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._get_json(f"/bridge{path}", params=params)

    async def bridge_post(self, path: str, json: Any = None) -> Any:
        return await self._post_json(f"/bridge{path}", json=json)

    async def clob_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._get_json(f"/clob{path}", params=params)

    async def clob_post(self, path: str, json: Any = None) -> Any:
        return await self._post_json(f"/clob{path}", json=json)

    async def clob_delete(self, path: str, json_body: Any = None) -> Any:
        if json_body is None:
            return await self._delete_json(f"/clob{path}")
        payload = json.dumps(json_body, separators=(",", ":"), ensure_ascii=False)
        return await self._delete_json(
            f"/clob{path}",
            content=payload.encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

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
