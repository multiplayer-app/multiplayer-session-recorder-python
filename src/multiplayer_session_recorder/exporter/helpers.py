from ..constants import (
    MULTIPLAYER_TRACE_DEBUG_PREFIX,
    MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX
)


def filter_spans_include_debug(spans_data):
    try:
        filtered_spans_data = type(spans_data)()
        
        for resource_span in spans_data.resource_spans:
            filtered_resource_span = type(resource_span)()
            filtered_resource_span.resource.CopyFrom(resource_span.resource)
            filtered_resource_span.scope_spans.extend([])
            
            for scope_span in resource_span.scope_spans:
                filtered_scope_span = type(scope_span)()
                filtered_scope_span.scope.CopyFrom(scope_span.scope)
                filtered_scope_span.spans.extend([])
                
                for span in scope_span.spans:
                    trace_id_str = format(span.trace_id, '032x')
                    if (trace_id_str.startswith(MULTIPLAYER_TRACE_DEBUG_PREFIX) or 
                        trace_id_str.startswith(MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX)):
                        filtered_scope_span.spans.extend([span])
                
                if filtered_scope_span.spans:
                    filtered_resource_span.scope_spans.extend([filtered_scope_span])
            
            if filtered_resource_span.scope_spans:
                filtered_spans_data.resource_spans.extend([filtered_resource_span])
        
        return filtered_spans_data
    except (IndexError, AttributeError):
        return spans_data


def filter_logs_include_debug(logs_data):
    try:
        filtered_logs_data = type(logs_data)()
        
        for resource_log in logs_data.resource_logs:
            filtered_resource_log = type(resource_log)()
            filtered_resource_log.resource.CopyFrom(resource_log.resource)
            filtered_resource_log.scope_logs.extend([])
            
            for scope_log in resource_log.scope_logs:
                filtered_scope_log = type(scope_log)()
                filtered_scope_log.scope.CopyFrom(scope_log.scope)
                filtered_scope_log.log_records.extend([])
                
                for log_record in scope_log.log_records:
                    trace_id_str = format(log_record.trace_id, '032x')
                    if (trace_id_str.startswith(MULTIPLAYER_TRACE_DEBUG_PREFIX) or 
                        trace_id_str.startswith(MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX)):
                        filtered_scope_log.log_records.extend([log_record])
                
                if filtered_scope_log.log_records:
                    filtered_resource_log.scope_logs.extend([filtered_scope_log])
            
            if filtered_resource_log.scope_logs:
                filtered_logs_data.resource_logs.extend([filtered_resource_log])
        
        return filtered_logs_data
    except (IndexError, AttributeError):
        return logs_data


def should_export_data(data, data_type="spans"):
    try:
        if data_type == "spans":
            return bool(data.resource_spans)
        elif data_type == "logs":
            return bool(data.resource_logs)
        else:
            return False
    except (IndexError, AttributeError):
        return False


def filter_spans_exclude_debug(spans_data):
    try:
        filtered_spans_data = type(spans_data)()
        
        for resource_span in spans_data.resource_spans:
            filtered_resource_span = type(resource_span)()
            filtered_resource_span.resource.CopyFrom(resource_span.resource)
            filtered_resource_span.scope_spans.extend([])
            
            for scope_span in resource_span.scope_spans:
                filtered_scope_span = type(scope_span)()
                filtered_scope_span.scope.CopyFrom(scope_span.scope)
                filtered_scope_span.spans.extend([])
                
                for span in scope_span.spans:
                    trace_id_str = format(span.trace_id, '032x')
                    if not (trace_id_str.startswith(MULTIPLAYER_TRACE_DEBUG_PREFIX) or 
                           trace_id_str.startswith(MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX)):
                        filtered_scope_span.spans.extend([span])
                
                if filtered_scope_span.spans:
                    filtered_resource_span.scope_spans.extend([filtered_scope_span])
            
            if filtered_resource_span.scope_spans:
                filtered_spans_data.resource_spans.extend([filtered_resource_span])
        
        return filtered_spans_data
    except (IndexError, AttributeError):
        return spans_data


def filter_logs_exclude_debug(logs_data):
    try:
        filtered_logs_data = type(logs_data)()
        
        for resource_log in logs_data.resource_logs:
            filtered_resource_log = type(resource_log)()
            filtered_resource_log.resource.CopyFrom(resource_log.resource)
            filtered_resource_log.scope_logs.extend([])
            
            for scope_log in resource_log.scope_logs:
                filtered_scope_log = type(scope_log)()
                filtered_scope_log.scope.CopyFrom(scope_log.scope)
                filtered_scope_log.log_records.extend([])
                
                for log_record in scope_log.log_records:
                    trace_id_str = format(log_record.trace_id, '032x')
                    if not (trace_id_str.startswith(MULTIPLAYER_TRACE_DEBUG_PREFIX) or 
                           trace_id_str.startswith(MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX)):
                        filtered_scope_log.log_records.extend([log_record])
                
                if filtered_scope_log.log_records:
                    filtered_resource_log.scope_logs.extend([filtered_scope_log])
            
            if filtered_resource_log.scope_logs:
                filtered_logs_data.resource_logs.extend([filtered_resource_log])
        
        return filtered_logs_data
    except (IndexError, AttributeError):
        return logs_data
