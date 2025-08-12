from dataclasses import dataclass, field
from typing import Callable, List, Optional
from opentelemetry.trace import Span


@dataclass
class HttpMiddlewareConfig:
    maxPayloadSizeBytes: Optional[int] = 4096

    captureHeaders: bool = True
    captureBody: bool = True

    isMaskBodyEnabled: bool = True
    isMaskHeadersEnabled: bool = True

    maskBody: Optional[Callable[[any, Span], any]] = None
    maskHeaders: Optional[Callable[[any, Span], any]] = None

    maskBodyFieldsList: List[str] = field(default_factory=list)
    maskHeadersList: List[str] = field(default_factory=list)

    headersToInclude: Optional[List[str]] = None
    headersToExclude: Optional[List[str]] = None
