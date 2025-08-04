from ..types.middleware_config import HttpMiddlewareConfig
from ..sdk.mask import mask as default_mask, sensitive_fields, sensitive_headers
from ..sdk.truncate import truncate
from ..constants import ATTR_MULTIPLAYER_HTTP_REQUEST_BODY, ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS, ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY, ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS


try:
    from flask import request, g
except ImportError:
    flask = None

from opentelemetry import trace
import json
from typing import Callable, Any


def FlaskOtelHttpPayloadRecorderMiddleware(config: HttpMiddlewareConfig):
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
        if config.captureBody:
            g.request_body = request.get_data(as_text=True)
        if config.captureHeaders:
            g.request_headers = dict(request.headers)

    def after_request(response):
        span = trace.get_current_span()

        if config.captureBody:
            body_raw = getattr(g, "request_body", "")
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

            try:
                resp_raw = response.get_data(as_text=True)
                parsed_resp = json.loads(resp_raw)
                masked_resp = (
                    body_mask_fn(parsed_resp, span) if body_mask_fn else json.dumps(parsed_resp)
                )
            except Exception:
                masked_resp = truncate(resp_raw, config.maxPayloadSizeBytes)

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY,
                truncate(masked_resp, config.maxPayloadSizeBytes)
            )

        if config.captureHeaders:
            req_headers = getattr(g, "request_headers", {})
            filtered_req_headers = {}

            for k, v in req_headers.items():
                k_l = k.lower()

                if config.headersToInclude and k_l not in config.headersToInclude:
                    continue
                if config.headersToExclude and k_l in config.headersToExclude:
                    continue

                if header_mask_fn:
                    masked = header_mask_fn({k: v}, span)
                    v = masked.get(k, v)

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
                    v = masked.get(k, v)

                filtered_resp_headers[k] = v

            span.set_attribute(
                ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS,
                str(filtered_resp_headers)
            )

        return response

    return before_request, after_request
