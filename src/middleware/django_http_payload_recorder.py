from ..types.middleware_config import HttpMiddlewareConfig
from ..sdk.mask import mask as default_mask, sensitive_fields, sensitive_headers
from ..sdk.truncate import truncate
from ..constants import ATTR_MULTIPLAYER_HTTP_REQUEST_BODY, ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS, ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY, ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS

import json
from django.utils.deprecation import MiddlewareMixin
from opentelemetry import trace

class DjangoOtelHttpPayloadRecorderMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None, config: HttpMiddlewareConfig = HttpMiddlewareConfig()):
        self.get_response = get_response
        self.config = config

        body_fields = self.config.maskBodyFieldsList or sensitive_fields
        header_fields = self.config.maskHeadersList or sensitive_headers

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
                    v = masked.get(k, v)

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
                    v = masked.get(k, v)

                captured_resp_headers[k] = v

            span.set_attribute(ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS, str(captured_resp_headers))

        return response
