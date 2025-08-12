from .capture_exception import capture_exception
from .mask import mask
from .set_attribute import (
    set_attribute,
    set_grpc_request_message,
    set_grpc_response_message,
    set_http_request_body, set_http_request_headers,
    set_http_response_body,
    set_http_response_headers,
    set_rpc_request_message,
    set_rpc_response_message,
    set_message_body
)

__all__ = [
    capture_exception,
    mask,
    set_attribute,
    set_grpc_request_message,
    set_grpc_response_message,
    set_http_request_body, set_http_request_headers,
    set_http_response_body,
    set_http_response_headers,
    set_rpc_request_message,
    set_rpc_response_message,
    set_message_body
]

class SessionRecorderSdk:
    capture_exception = capture_exception
    mask = mask
    set_attribute = set_attribute
    set_grpc_request_message = set_grpc_request_message
    set_grpc_response_message = set_grpc_response_message
    set_http_request_body = set_http_request_body
    set_http_request_headers = set_http_request_headers
    set_http_response_body = set_http_response_body
    set_http_response_headers = set_http_response_headers
    set_rpc_request_message = set_rpc_request_message
    set_rpc_response_message = set_rpc_response_message
    set_message_body = set_message_body
