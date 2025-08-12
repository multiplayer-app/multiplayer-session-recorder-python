from opentelemetry.sdk.trace.sampling import Sampler, Decision, SamplingResult, _get_parent_trace_state
from opentelemetry.context import Context
from opentelemetry.trace.span import TraceState
from typing import Optional, Sequence
from opentelemetry.trace import Link, SpanKind
from opentelemetry.util.types import Attributes
from ..constants import MULTIPLAYER_TRACE_DEBUG_PREFIX, MULTIPLAYER_TRACE_DOC_PREFIX

class SessionRecorderTraceIdRatioBasedSampler(Sampler):
    """
    Sampler that makes sampling decisions probabilistically based on `rate`.

    Args:
        rate: Probability (between 0 and 1) that a span will be sampled
    """

    def __init__(self, rate: float):
        if rate < 0.0 or rate > 1.0:
            raise ValueError("Probability must be in range [0.0, 1.0].")
        self._rate = rate
        self._bound = self.get_bound_for_rate(self._rate)

    # For compatibility with 64 bit trace IDs, the sampler checks the 64
    # low-order bits of the trace ID to decide whether to sample a given trace.
    TRACE_ID_LIMIT = (1 << 64) - 1

    @classmethod
    def get_bound_for_rate(cls, rate: float) -> int:
        return round(rate * (cls.TRACE_ID_LIMIT + 1))

    @property
    def rate(self) -> float:
        return self._rate

    @property
    def bound(self) -> int:
        return self._bound

    def should_sample(
        self,
        parent_context: Optional["Context"],
        trace_id: int,
        name: Optional[str] = None,
        kind: Optional[SpanKind] = None,
        attributes: Attributes = None,
        links: Optional[Sequence["Link"]] = None,
        trace_state: Optional["TraceState"] = None,
    ) -> "SamplingResult":
        decision = Decision.DROP
        trace_id_str = trace_id.__str__()
        if trace_id_str.startswith(MULTIPLAYER_TRACE_DEBUG_PREFIX) or trace_id_str.startswith(MULTIPLAYER_TRACE_DOC_PREFIX):
            decision = Decision.RECORD_AND_SAMPLE
        if trace_id & self.TRACE_ID_LIMIT < self.bound:
            decision = Decision.RECORD_AND_SAMPLE
        if decision is Decision.DROP:
            attributes = None
        return SamplingResult(
            decision,
            attributes,
            _get_parent_trace_state(parent_context),
        )

    def get_description(self) -> str:
        return f"SessionRecorderTraceIdRatioBased{{{self._rate}}}"
