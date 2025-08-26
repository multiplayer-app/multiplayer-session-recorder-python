import os
from typing import Optional
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as BaseOTLPSpanExporter
from ...constants import MULTIPLAYER_OTEL_DEFAULT_TRACES_EXPORTER_HTTP_URL
from ..helpers import filter_spans_include_debug, should_export_data

class OTLPSpanExporter(BaseOTLPSpanExporter):
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        **kwargs
    ):
        if api_key is None:
            api_key = os.getenv("MULTIPLAYER_OTLP_KEY")

        if endpoint is None:
            endpoint = MULTIPLAYER_OTEL_DEFAULT_TRACES_EXPORTER_HTTP_URL
        
        headers = {"authorization": api_key}
        
        super().__init__(
            endpoint=endpoint,
            headers=headers,
            **kwargs
        )
    
    def export(self, spans_data, **kwargs):
        filtered_spans_data = filter_spans_include_debug(spans_data)
        
        if not should_export_data(filtered_spans_data, "spans"):
            return None
        
        return super().export(filtered_spans_data, **kwargs)


def create_http_span_exporter(
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    **kwargs
) -> OTLPSpanExporter:
    return OTLPSpanExporter(api_key=api_key, endpoint=endpoint, **kwargs)
