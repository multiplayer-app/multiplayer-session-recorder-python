from opentelemetry import trace
from opentelemetry.trace import Span
from typing import Any, Dict
from .mask import mask
from ..constants import ATTR_MULTIPLAYER_HTTP_REQUEST_BODY, ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS, ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY, ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS, ATTR_MULTIPLAYER_RPC_REQUEST_MESSAGE, ATTR_MULTIPLAYER_RPC_RESPONSE_MESSAGE, ATTR_MULTIPLAYER_GRPC_REQUEST_MESSAGE, ATTR_MULTIPLAYER_GRPC_RESPONSE_MESSAGE, ATTR_MULTIPLAYER_MESSAGING_MESSAGE_BODY

sensitive_fields = ["password", "token", "authorization"]
sensitive_headers = ["authorization", "cookie"]

def _get_active_span() -> Span:
    span = trace.get_current_span()
    if span is None or not span.is_recording():
        return None
    return span

def set_attribute(key: str, value: Any) -> None:
    span = _get_active_span()
    if span:
        span.set_attribute(key, value)

def _set_masked_attribute(key: str, body: Any, mask_keys, do_mask: bool) -> None:
    span = _get_active_span()
    if not span:
        return

    if do_mask:
        body = mask(mask_keys)(body, span)

    span.set_attribute(key, body)

def set_http_request_body(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_HTTP_REQUEST_BODY, body, sensitive_fields, options.get("mask", True))

def set_http_request_headers(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS, body, sensitive_headers, options.get("mask", True))

def set_http_response_body(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY, body, sensitive_fields, options.get("mask", True))

def set_http_response_headers(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS, body, sensitive_fields, options.get("mask", True))

def set_message_body(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_MESSAGING_MESSAGE_BODY, body, sensitive_fields, options.get("mask", True))

def set_rpc_request_message(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_RPC_REQUEST_MESSAGE, body, sensitive_fields, options.get("mask", True))

def set_rpc_response_message(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_RPC_RESPONSE_MESSAGE, body, sensitive_fields, options.get("mask", True))

def set_grpc_request_message(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_GRPC_REQUEST_MESSAGE, body, sensitive_fields, options.get("mask", True))

def set_grpc_response_message(body: Any, options: Dict[str, bool] = {"mask": True}) -> None:
    _set_masked_attribute(ATTR_MULTIPLAYER_GRPC_RESPONSE_MESSAGE, body, sensitive_fields, options.get("mask", True))
