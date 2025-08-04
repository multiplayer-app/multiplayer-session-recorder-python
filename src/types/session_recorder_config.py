from dataclasses import dataclass
from typing import Optional, Union, Callable
from ..trace.id_generator import SessionRecorderRandomIdGenerator

@dataclass
class SessionRecorderConfig:
    apiKey: str
    traceIdGenerator: SessionRecorderRandomIdGenerator
    resourceAttributes: Optional[dict] = None
    generateSessionShortIdLocally: Union[bool, Callable[[], str], None] = None
