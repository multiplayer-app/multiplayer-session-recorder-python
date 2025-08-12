# import json
import aiohttp
import asyncio
from typing import Optional, Dict, Any, List, Union
from ..constants import MULTIPLAYER_BASE_API_URL

class ApiServiceConfig:
    def __init__(
        self,
        apiKey: Optional[str] = None,
        exporter_api_base_url: Optional[str] = None,
        continuous_debugging: Optional[bool] = False,
    ):
        self.apiKey = apiKey
        self.exporter_api_base_url = exporter_api_base_url or MULTIPLAYER_BASE_API_URL
        self.continuous_debugging = continuous_debugging

class ApiService:
    def __init__(self):
        self.config = ApiServiceConfig()

    def init(self, config: Dict[str, Any]):
        for key, value in config.items():
            setattr(self.config, key, value)

    def update_configs(self, config: Dict[str, Any]):
        for key, value in config.items():
            setattr(self.config, key, value)

    async def start_session(
        self,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return await self._make_request("/debug-sessions/start", "POST", request_body)

    async def stop_session(
        self,
        session_id: str,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return await self._make_request(f"/debug-sessions/{session_id}/stop", "PATCH", request_body)

    async def cancel_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return await self._make_request(f"/debug-sessions/{session_id}/cancel", "DELETE")

    async def start_continuous_session(
        self,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return await self._make_request("/continuous-debug-sessions/start", "POST", request_body)

    async def save_continuous_session(
        self,
        session_id: str,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return await self._make_request(f"/continuous-debug-sessions/{session_id}/save", "POST", request_body)

    async def stop_continuous_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return await self._make_request(f"/continuous-debug-sessions/{session_id}/cancel", "DELETE")

    async def check_remote_session(
        self,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return await self._make_request("/remote-debug-session/check", "POST", request_body)

    async def _make_request(
        self,
        path: str,
        method: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        url = f"{self.config.exporter_api_base_url}/v0/radar{path}"
        headers = {
            "Content-Type": "application/json",
        }

        if self.config.apiKey:
            headers["X-Api-Key"] = self.config.apiKey

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body,
                ) as response:
                    if not response.ok:
                        raise Exception(f"Request failed: {response.status} {response.reason}")

                    if response.status == 204:
                        return None

                    return await response.json()

        except aiohttp.ClientError as e:
            if isinstance(e, aiohttp.ClientTimeout):
                raise Exception("Request timed out")
            elif isinstance(e, aiohttp.ClientConnectionError):
                raise Exception("Connection error")
            raise Exception(f"Request error: {str(e)}")
        except Exception as e:
            raise Exception(f"Request error: {str(e)}")
