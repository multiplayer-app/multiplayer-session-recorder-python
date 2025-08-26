import os
from typing import Optional
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter as BaseOTLPLogExporter

from ...constants import MULTIPLAYER_OTEL_DEFAULT_LOGS_EXPORTER_GRPC_URL
from ..helpers import filter_logs_include_debug, should_export_data

class OTLPLogExporter(BaseOTLPLogExporter):
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        **kwargs
    ):
        if api_key is None:
            api_key = os.getenv("MULTIPLAYER_OTLP_KEY")
        
        if endpoint is None:
            endpoint = MULTIPLAYER_OTEL_DEFAULT_LOGS_EXPORTER_GRPC_URL
        
        headers = {"authorization": api_key}
        
        super().__init__(
            endpoint=endpoint,
            headers=headers,
            **kwargs
        )
    
    def export(self, logs_data, **kwargs):
        filtered_logs_data = filter_logs_include_debug(logs_data)
        
        if not should_export_data(filtered_logs_data, "logs"):
            return None
        
        return super().export(filtered_logs_data, **kwargs)


def create_grpc_log_exporter(
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    **kwargs
) -> OTLPLogExporter:
    return OTLPLogExporter(api_key=api_key, endpoint=endpoint, **kwargs)
