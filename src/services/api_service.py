# import json
import requests
from typing import Optional, Dict, Any, List, Union
from ..constants import MULTIPLAYER_BASE_API_URL

class ApiServiceConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        exporter_api_base_url: Optional[str] = None,
        continuous_debugging: Optional[bool] = False,
    ):
        self.api_key = api_key
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

    def start_session(
        self,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self._make_request("/debug-sessions/start", "POST", request_body)

    def stop_session(
        self,
        session_id: str,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self._make_request(f"/debug-sessions/{session_id}/stop", "PATCH", request_body)

    def cancel_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._make_request(f"/debug-sessions/{session_id}/cancel", "DELETE")

    def start_continuous_session(
        self,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self._make_request("/continuous-debug-sessions/start", "POST", request_body)

    def save_continuous_session(
        self,
        session_id: str,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self._make_request(f"/continuous-debug-sessions/{session_id}/save", "POST", request_body)

    def stop_continuous_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._make_request(f"/continuous-debug-sessions/{session_id}/cancel", "DELETE")

    def check_remote_session(
        self,
        request_body: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self._make_request("/remote-debug-session/check", "POST", request_body)

    def _make_request(
        self,
        path: str,
        method: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        url = f"{self.config.exporter_api_base_url}/v0/radar{path}"
        headers = {
            "Content-Type": "application/json",
        }

        if self.config.api_key:
            headers["X-Api-Key"] = self.config.api_key

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=body,
                cookies={},  # Add cookies if needed
                timeout=10,
            )

            if not response.ok:
                raise Exception(f"Request failed: {response.status_code} {response.reason}")

            if response.status_code == 204:
                return None

            return response.json()

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.Timeout):
                raise Exception("Request timed out")
            elif isinstance(e, requests.exceptions.ConnectionError):
                raise Exception("Connection error")
            raise Exception(f"Request error: {str(e)}")
