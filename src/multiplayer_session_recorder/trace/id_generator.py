import random
from opentelemetry import trace
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
from ..types.session_type import SessionType
from ..constants import MULTIPLAYER_TRACE_DEBUG_PREFIX, MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX

class SessionRecorderRandomIdGenerator(RandomIdGenerator):
    def __init__(self):
        super().__init__()
        self.session_type = ''
        self.session_short_id = ''
    
    def set_session_id(self, session_short_id: str, session_type: SessionType) -> None:
        self.session_short_id = session_short_id
        self.session_type = session_type

    def generate_span_id(self) -> int:
        span_id = random.getrandbits(64)
        while span_id == trace.INVALID_SPAN_ID:
            span_id = random.getrandbits(64)
        return span_id

    def generate_trace_id(self) -> int:
        trace_id = random.getrandbits(128)
        while trace_id == trace.INVALID_TRACE_ID:
            trace_id = random.getrandbits(128)

        if self.session_short_id:
            session_type_prefix = ""

            if self.session_type == SessionType.CONTINUOUS:
                session_type_prefix = MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX
            else:
                session_type_prefix = MULTIPLAYER_TRACE_DEBUG_PREFIX

            prefix = f"{session_type_prefix}{self.session_short_id}"

            session_trace_id = f"{prefix}{trace_id[len(prefix):]}"

            return session_trace_id

        return trace_id
