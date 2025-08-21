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

import json
from typing import Optional
from opentelemetry import trace


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

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    raise ImportError(
        "Django is required for Django middleware. "
        "Install it with: pip install multiplayer-session-recorder[django]"
    )

class DjangoOtelHttpPayloadRecorderMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None, config: Optional[HttpMiddlewareConfig] = None):
        if config is None:
            config = HttpMiddlewareConfig()
        self.get_response = get_response
        self.config = config

        body_fields = self.config.maskBodyFieldsList if self.config.maskBodyFieldsList else sensitive_fields
        header_fields = self.config.maskHeadersList if self.config.maskHeadersList else sensitive_headers

        if config.isMaskBodyEnabled:
            if config.maskBody:
                self.body_mask_fn = config.maskBody
            else:
                self.body_mask_fn = default_mask(body_fields)

        if config.isMaskHeadersEnabled:
            if config.maskHeaders:
                self.header_mask_fn = config.maskHeaders
            else:
                self.header_mask_fn = default_mask(header_fields)

    def __call__(self, request):
        span = trace.get_current_span()

        if not hasattr(span, 'set_attribute') or not span.is_recording():
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(f"django_request_{request.method}_{request.path}") as span:
                if _should_capture_payloads(span):
                    return self._process_request(request, span)
                else:
                    return self.get_response(request)
        else:
            if _should_capture_payloads(span):
                return self._process_request(request, span)
            else:
                return self.get_response(request)

    def _process_request(self, request, span):

        # --- Capture request body ---
        if self.config.captureBody:
            try:
                body_raw = request.body.decode("utf-8")
                try:
                    parsed = json.loads(body_raw)
                    masked = (
                        self.body_mask_fn(parsed, span)
                        if self.body_mask_fn else json.dumps(parsed)
                    )
                except Exception:
                    masked = body_raw
                span.set_attribute(
                    ATTR_MULTIPLAYER_HTTP_REQUEST_BODY,
                    truncate(masked, self.config.maxPayloadSizeBytes)
                )
            except Exception:
                pass

        # --- Capture request headers ---
        if self.config.captureHeaders:
            headers = request.headers if hasattr(request, "headers") else request.META
            captured_headers = {}
            for k, v in headers.items():
                k_l = k.lower()

                if self.config.headersToInclude and k_l not in self.config.headersToInclude:
                    continue
                if self.config.headersToExclude and k_l in self.config.headersToExclude:
                    continue

                if self.header_mask_fn:
                    masked = self.header_mask_fn({k: v}, span)
                    # The mask function returns a string, so we need to parse it back to get the masked value
                    try:
                        masked_dict = json.loads(masked)
                        v = masked_dict.get(k, v)
                    except (json.JSONDecodeError, AttributeError):
                        # If parsing fails, use the original value
                        v = v

                captured_headers[k] = v

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS,
                str(captured_headers)
            )

        # Get response
        response = self.get_response(request)

        # --- Capture response body ---
        if self.config.captureBody:
            try:
                resp_body = response.content.decode("utf-8")
                try:
                    parsed_resp = json.loads(resp_body)
                    masked_resp = (
                        self.body_mask_fn(parsed_resp, span)
                        if self.body_mask_fn else json.dumps(parsed_resp)
                    )
                except Exception:
                    masked_resp = resp_body

                span.set_attribute(ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY, truncate(masked_resp, self.config.maxPayloadSizeBytes))
            except Exception:
                pass

        # --- Capture response headers ---
        if self.config.captureHeaders:
            captured_resp_headers = {}
            for k, v in response.items():
                k_l = k.lower()

                if self.config.headersToInclude and k_l not in self.config.headersToInclude:
                    continue
                if self.config.headersToExclude and k_l in self.config.headersToExclude:
                    continue

                if self.header_mask_fn:
                    masked = self.header_mask_fn({k: v}, span)
                    # The mask function returns a string, so we need to parse it back to get the masked value
                    try:
                        masked_dict = json.loads(masked)
                        v = masked_dict.get(k, v)
                    except (json.JSONDecodeError, AttributeError):
                        # If parsing fails, use the original value
                        v = v

                captured_resp_headers[k] = v

            span.set_attribute(ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS, str(captured_resp_headers))

        return response
