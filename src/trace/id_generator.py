import random
from opentelemetry import trace
from opentelemetry.sdk.trace.sampling import Decision
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
from .sampler import SessionRecorderTraceIdRatioBasedSampler
from ..constants import MULTIPLAYER_TRACE_DOC_PREFIX

class SessionRecorderRandomIdGenerator(RandomIdGenerator):
    def __init__(self, autoDocTracesRatio: float = 0):
        super().__init__()
        self.autoDocTracesRatio = autoDocTracesRatio
        self.docSpanSampler = SessionRecorderTraceIdRatioBasedSampler(autoDocTracesRatio)

    def generate_span_id(self) -> int:
        span_id = random.getrandbits(64)
        while span_id == trace.INVALID_SPAN_ID:
            span_id = random.getrandbits(64)
        return span_id

    def generate_trace_id(self) -> int:
        trace_id = random.getrandbits(128)
        while trace_id == trace.INVALID_TRACE_ID:
            trace_id = random.getrandbits(128)

        if self._isDocTrace(trace_id):
            return int(f"{MULTIPLAYER_TRACE_DOC_PREFIX}{hex(trace_id)[8:]}", 16)

        return trace_id

    def _isDocTrace(self, trace_id: str) -> bool:
        return self.docSpanSampler.should_sample(None, trace_id).decision == Decision.RECORD_AND_SAMPLE
