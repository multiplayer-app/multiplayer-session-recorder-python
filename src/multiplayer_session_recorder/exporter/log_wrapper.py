from typing import Optional
from opentelemetry.sdk.logs.export import LogExporter
from .helpers import filter_logs_exclude_debug, should_export_data

class OTLPLogExporterWrapper:
    def __init__(self, exporter: LogExporter):
        self.exporter = exporter
    
    def export(self, logs_data, **kwargs):
        
        
        filtered_logs_data = filter_logs_exclude_debug(logs_data)
        
        if not should_export_data(filtered_logs_data, "logs"):
            return None

        return self.exporter.export(filtered_logs_data, **kwargs)
    
    def __getattr__(self, name):
        """
        Delegate all other attributes to the underlying exporter.
        """
        return getattr(self.exporter, name)
