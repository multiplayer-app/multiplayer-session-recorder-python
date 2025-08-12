from typing import Any, Callable, Dict, Optional, Union
from datetime import datetime
from ..constants import MULTIPLAYER_TRACE_DEBUG_SESSION_SHORT_ID_LENGTH
from ..trace.id_generator import SessionRecorderRandomIdGenerator
from ..services.api_service import ApiService
from ..sdk.session_id_generator import generate_session_short_id
from ..types.session_recorder_config import SessionRecorderConfig
from ..types.session_type import SessionType

def get_formatted_date(date: float, options: Optional[dict] = None) -> str:
    dt = datetime.fromtimestamp(date / 1000.0)
    return dt.strftime('%b %d, %Y, %H:%M:%S')

class SessionRecorder:
    def __init__(self):
        self._is_initialized = False
        self._short_session_id: Union[str, bool] = False
        self._trace_id_generator: Optional[SessionRecorderRandomIdGenerator] = None
        self._session_type: SessionType = SessionType.PLAIN
        self._session_state: str = 'STOPPED'  # 'STARTED', 'STOPPED', 'PAUSED'
        self._api_service = ApiService()
        self._session_short_id_generator = generate_session_short_id
        self._resource_attributes: Dict[str, Any] = {}

    def init(self, config: Union[SessionRecorderConfig, Dict[str, Any]] = None, **kwargs) -> None:
        # Handle both dictionary config and keyword arguments
        if config is not None:
            # Convert dict to SessionRecorderConfig if needed
            if isinstance(config, dict):
                config = SessionRecorderConfig(**config)
        else:
            # Use keyword arguments
            config = SessionRecorderConfig(**kwargs)
            
        self._resource_attributes = config.resourceAttributes or {}
        self._is_initialized = True

        if callable(config.generateSessionShortIdLocally):
            self._session_short_id_generator = config.generateSessionShortIdLocally

        if not config.apiKey:
            raise ValueError('Api key not provided')

        trace_id_generator = config.traceIdGenerator
        if not hasattr(trace_id_generator, 'session_short_id'):
            raise ValueError('Incompatible trace id generator')

        self._trace_id_generator = trace_id_generator
        self._api_service.init({'apiKey': config.apiKey})

    async def start(self, session_type: SessionType, session_payload: Optional[Dict[str, Any]] = None) -> None:
        if not self._is_initialized:
            raise RuntimeError('Configuration not initialized. Call init() before performing any actions.')

        if session_payload and session_payload.get('shortId') and \
           len(session_payload['shortId']) != MULTIPLAYER_TRACE_DEBUG_SESSION_SHORT_ID_LENGTH:
            raise ValueError('Invalid short session id')

        session_payload = session_payload or {}

        if self._session_state != 'STOPPED':
            raise RuntimeError('Session should be ended before starting new one.')

        self._session_type = session_type

        session_payload['name'] = session_payload.get('name') or f"Session on {get_formatted_date(datetime.now().timestamp() * 1000)}"
        session_payload['resourceAttributes'] = {
            **self._resource_attributes,
            **session_payload.get('resourceAttributes', {})
        }

        if self._session_type == SessionType.CONTINUOUS:
            session = await self._api_service.start_continuous_session(session_payload)
        else:
            session = await self._api_service.start_session(session_payload)

        self._short_session_id = session['shortId']
        self._trace_id_generator.set_session_id(self._short_session_id, self._session_type)
        self._session_state = 'STARTED'

    async def save(self, session_data: Optional[Dict[str, Any]] = None) -> None:
        if not self._is_initialized:
            raise RuntimeError('Configuration not initialized. Call init() before performing any actions.')
        if self._session_state == 'STOPPED' or not isinstance(self._short_session_id, str):
            raise RuntimeError('Session should be active or paused')
        if self._session_type != SessionType.CONTINUOUS:
            raise RuntimeError('Invalid session type')
        await self._api_service.save_continuous_session(
            self._short_session_id,
            {
                **(session_data or {}),
                'name': (session_data or {}).get('name') or f"Session on {get_formatted_date(datetime.now().timestamp() * 1000)}"
            }
        )

    async def stop(self, session_data: Optional[Dict[str, Any]] = None) -> None:
        try:
            if not self._is_initialized:
                raise RuntimeError('Configuration not initialized. Call init() before performing any actions.')
            if self._session_state == 'STOPPED' or not isinstance(self._short_session_id, str):
                raise RuntimeError('Session should be active or paused')
            if self._session_type != SessionType.PLAIN:
                raise RuntimeError('Invalid session type')
            await self._api_service.stop_session(self._short_session_id, session_data or {})
        finally:
            self._trace_id_generator.set_session_id('', SessionType.PLAIN)
            self._short_session_id = False
            self._session_state = 'STOPPED'

    async def cancel(self) -> None:
        try:
            if not self._is_initialized:
                raise RuntimeError('Configuration not initialized. Call init() before performing any actions.')
            if self._session_state == 'STOPPED' or not isinstance(self._short_session_id, str):
                raise RuntimeError('Session should be active or paused')
            if self._session_type == SessionType.CONTINUOUS:
                await self._api_service.stop_continuous_session(self._short_session_id)
            elif self._session_type == SessionType.PLAIN:
                await self._api_service.cancel_session(self._short_session_id)
        finally:
            self._trace_id_generator.set_session_id('', SessionType.PLAIN)
            self._short_session_id = False
            self._session_state = 'STOPPED'

    async def auto_start_remote_continuous_session(self, session_payload: Optional[Dict[str, Any]] = None) -> None:
        if not self._is_initialized:
            raise RuntimeError('Configuration not initialized. Call init() before performing any actions.')
        session_payload = session_payload or {}
        session_payload['resourceAttributes'] = {
            **session_payload.get('resourceAttributes', {}),
            **self._resource_attributes,
        }
        result = await self._api_service.check_remote_session(session_payload)
        should_start = result.get('shouldStart', False)
        if self._session_state != 'STOPPED':
            raise RuntimeError('Session should be ended before starting new one.')
        if not should_start:
            return
        self._session_type = SessionType.CONTINUOUS
        self._short_session_id = self._session_short_id_generator()
        session_payload['name'] = session_payload.get('name') or f"Session on {get_formatted_date(datetime.now().timestamp() * 1000)}"
        session_payload['resourceAttributes'] = {
            **self._resource_attributes,
            **session_payload.get('resourceAttributes', {})
        }
        session = await self._api_service.start_continuous_session(session_payload)
        self._short_session_id = session['shortId']
        self._trace_id_generator.set_session_id(self._short_session_id, self._session_type)
        self._session_state = 'STARTED' 
