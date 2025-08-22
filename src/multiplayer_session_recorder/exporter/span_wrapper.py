from typing import Optional
from opentelemetry.sdk.trace.export import SpanExporter
from .helpers import filter_spans_exclude_debug, should_export_data

class OTLPSpanExporterWrapper:
    def __init__(self, exporter: SpanExporter):
        """
        Initialize the wrapper with an existing span exporter.
        
        Args:
            exporter: The span exporter to wrap with filtering
        """
        self.exporter = exporter

    def export(self, spans_data, **kwargs):
        filtered_spans_data = filter_spans_exclude_debug(spans_data)
        
        if not should_export_data(filtered_spans_data, "spans"):
            return None
        
        return self.exporter.export(filtered_spans_data, **kwargs)
    
    def __getattr__(self, name):
        return getattr(self.exporter, name)
