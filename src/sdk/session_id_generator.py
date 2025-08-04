import random
from opentelemetry import trace
from opentelemetry.sdk.trace.sampling import Decision
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator

INVALID_SESSION_ID = 0x00000000

def generate_session_short_id() -> str:
    session_shrot_id = random.getrandbits(32)
    while session_shrot_id == trace.INVALID_SESSION_ID:
        session_shrot_id = random.getrandbits(32)

    return str(session_shrot_id)
