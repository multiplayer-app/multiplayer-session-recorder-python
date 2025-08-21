from ..types.middleware_config import HttpMiddlewareConfig
from ..sdk.mask import mask as default_mask, sensitive_fields, sensitive_headers
from ..sdk.truncate import truncate
from ..constants import (
    ATTR_MULTIPLAYER_HTTP_REQUEST_BODY,
    ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS,
    ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY,
    ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS,
    MULTIPLAYER_TRACE_DEBUG_PREFIX,
    MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX
)

try:
    from flask import request, g
except ImportError:
    raise ImportError(
        "Flask is required for Flask middleware. "
        "Install it with: pip install multiplayer-session-recorder[flask]"
    )

from opentelemetry import trace
import json
from typing import Callable, Any, Optional


def _should_capture_payloads(span) -> bool:
    if not hasattr(span, 'get_span_context'):
        return False
    
    span_context = span.get_span_context()
    if not span_context.is_valid:
        return False
    
    trace_id = span_context.trace_id
    trace_id_str = format(trace_id, '032x')  # Convert to 32-character hex string
    
    return (trace_id_str.startswith(MULTIPLAYER_TRACE_DEBUG_PREFIX) or 
            trace_id_str.startswith(MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX))

def FlaskOtelHttpPayloadRecorderMiddleware(config: Optional[HttpMiddlewareConfig] = None):
    if config is None:
        config = HttpMiddlewareConfig()
    final_body_keys = (
        config.maskBodyFieldsList
        if isinstance(config.maskBodyFieldsList, list)
        else sensitive_fields
    )

    final_header_keys = (
        config.maskHeadersList
        if isinstance(config.maskHeadersList, list)
        else sensitive_headers
    )

    body_mask_fn: Callable[[Any, Any], str] = None
    header_mask_fn: Callable[[Any, Any], str] = None

    if config.isMaskBodyEnabled:
        if config.maskBody:
            body_mask_fn = config.maskBody
        else:
            body_mask_fn = default_mask(final_body_keys)

    if config.isMaskHeadersEnabled:
        if config.maskHeaders:
            header_mask_fn = config.maskHeaders
        else:
            header_mask_fn = default_mask(final_header_keys)

    def before_request():
        # Get the current span to store request data
        span = trace.get_current_span()
        
        # Check if we have a valid span and should capture payloads
        if not hasattr(span, 'set_attribute') or not _should_capture_payloads(span):
            return
        
        if config.captureBody:
            # Capture request body without consuming the stream
            try:
                # Try with copy=True first, fallback to without if not supported
                try:
                    request_body = request.get_data(as_text=True, copy=True)
                except TypeError:
                    # Fallback for older Flask versions that don't support copy=True
                    request_body = request.get_data(as_text=True)
                # Store in Flask g object for this request (thread-safe)
                g._request_body = request_body
            except Exception:
                g._request_body = ""
        if config.captureHeaders:
            request_headers = dict(request.headers)
            # Store in Flask g object for this request (thread-safe)
            g._request_headers = request_headers

    def after_request(response):
        span = trace.get_current_span()

        # Check if we have a valid span and should capture payloads
        if not hasattr(span, 'set_attribute') or not _should_capture_payloads(span):
            return response

        if config.captureBody:
            body_raw = getattr(g, "_request_body", "") or ""
            try:
                parsed = json.loads(body_raw)
                masked_body = (
                    body_mask_fn(parsed, span) if body_mask_fn else json.dumps(parsed)
                )
            except Exception:
                masked_body = truncate(body_raw, config.maxPayloadSizeBytes)

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_REQUEST_BODY,
                truncate(masked_body, config.maxPayloadSizeBytes)
            )

        if config.captureBody:
            try:
                if hasattr(response, 'get_data'):
                    try:
                        try:
                            resp_data = response.get_data(copy=True)
                        except TypeError:
                            resp_data = response.get_data()
                        resp_raw = resp_data.decode('utf-8') if isinstance(resp_data, bytes) else str(resp_data)
                    except Exception as e:
                        resp_raw = ""
                elif hasattr(response, 'data'):
                    resp_raw = str(response.data)
                elif hasattr(response, 'response'):
                    resp_raw = str(response.response)
                else:
                    resp_raw = str(response)
                
                # Try to parse as JSON for masking
                try:
                    parsed_resp = json.loads(resp_raw)
                    masked_resp = (
                        body_mask_fn(parsed_resp, span) if body_mask_fn else json.dumps(parsed_resp)
                    )
                except json.JSONDecodeError:
                    # If not JSON, use the raw text
                    masked_resp = resp_raw
                    
            except Exception as e:
                masked_resp = ""

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY,
                truncate(masked_resp, config.maxPayloadSizeBytes)
            )

        if config.captureHeaders:
            req_headers = getattr(g, "_request_headers", {}) or {}
                
            filtered_req_headers = {}

            for k, v in req_headers.items():
                k_l = k.lower()

                if config.headersToInclude and k_l not in config.headersToInclude:
                    continue
                if config.headersToExclude and k_l in config.headersToExclude:
                    continue

                if header_mask_fn:
                    masked = header_mask_fn({k: v}, span)
                    try:
                        masked_dict = json.loads(masked)
                        v = masked_dict.get(k, v)
                    except (json.JSONDecodeError, AttributeError):
                        v = v

                filtered_req_headers[k] = v

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS,
                str(filtered_req_headers)
            )

        if config.captureHeaders:
            filtered_resp_headers = {}

            for k, v in response.headers.items():
                k_l = k.lower()

                if config.headersToInclude and k_l not in config.headersToInclude:
                    continue
                if config.headersToExclude and k_l in config.headersToExclude:
                    continue

                if header_mask_fn:
                    masked = header_mask_fn({k: v}, span)
                    try:
                        masked_dict = json.loads(masked)
                        v = masked_dict.get(k, v)
                    except (json.JSONDecodeError, AttributeError):
                        v = v

                filtered_resp_headers[k] = v

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS,
                str(filtered_resp_headers)
            )

        return response

    return before_request, after_request
