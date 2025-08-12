from .sdk import SessionRecorderSdk
from .session_recorder import SessionRecorder
from .trace.id_generator import SessionRecorderRandomIdGenerator
from .trace.sampler import SessionRecorderTraceIdRatioBasedSampler
from .types.session_type import SessionType

from .middleware import (
    create_django_middleware,
    create_flask_middleware,
    is_django_available,
    is_flask_available
)

session_recorder = SessionRecorder()

__all__ = [
    SessionRecorderRandomIdGenerator,
    SessionRecorderTraceIdRatioBasedSampler, 
    SessionRecorderSdk,
    SessionType,
    session_recorder,
    create_django_middleware,
    create_flask_middleware,
    is_django_available,
    is_flask_available
]

# Conditionally expose middleware classes if available
try:
    from .middleware.django_http_payload_recorder import DjangoOtelHttpPayloadRecorderMiddleware
    __all__.append("DjangoOtelHttpPayloadRecorderMiddleware")
except ImportError:
    pass

try:
    from .middleware.flask_http_payload_recorder import FlaskOtelHttpPayloadRecorderMiddleware
    __all__.append("FlaskOtelHttpPayloadRecorderMiddleware")
except ImportError:
    pass
