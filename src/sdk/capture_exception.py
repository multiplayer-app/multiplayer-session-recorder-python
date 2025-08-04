from opentelemetry import trace, context
from opentelemetry.trace import Span, StatusCode

def capture_exception(error: Exception) -> None:
    if not error:
        return

    span: Span = trace.get_current_span()
    if not span or not span.is_recording():
        return

    span.record_exception(error)
    span.set_status(StatusCode.ERROR, str(error))
