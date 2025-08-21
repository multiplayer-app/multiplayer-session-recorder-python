from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from multiplayer_session_recorder.trace.id_generator import SessionRecorderRandomIdGenerator
from multiplayer_session_recorder.trace.sampler import SessionRecorderTraceIdRatioBasedSampler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import (
    SERVICE_NAME as SERVICE_NAME_ATTR,
    SERVICE_VERSION as SERVICE_VERSION_ATTR,
    DEPLOYMENT_ENVIRONMENT,
    Resource
)
from config import (
    OTLP_TRACES_ENDPOINT,
    OTLP_LOGS_ENDPOINT,
    MULTIPLAYER_OTLP_KEY,
    MULTIPLAYER_OTLP_SPAN_RATIO,
    SERVICE_NAME,
    SERVICE_VERSION,
    PLATFORM_ENV
)

def init_opentelemetry():
    resource = Resource(attributes = {
        SERVICE_NAME_ATTR: SERVICE_NAME,
        SERVICE_VERSION_ATTR: SERVICE_VERSION,
        DEPLOYMENT_ENVIRONMENT: PLATFORM_ENV
    })
        
    id_generator = SessionRecorderRandomIdGenerator()
    sampler = SessionRecorderTraceIdRatioBasedSampler(rate = MULTIPLAYER_OTLP_SPAN_RATIO)

    traceExporter = OTLPSpanExporter(endpoint = OTLP_TRACES_ENDPOINT)
    logExporter = OTLPLogExporter(endpoint = OTLP_LOGS_ENDPOINT)

    tracer_provider = TracerProvider(
        resource = resource,
        sampler = sampler,
        id_generator = id_generator
    )

    logger_provider = LoggerProvider(resource = resource)
    set_logger_provider(logger_provider)

    logger_provider.add_log_record_processor(BatchLogRecordProcessor(logExporter))

    span_processor = BatchSpanProcessor(traceExporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
    
    print(f"OpenTelemetry initialized. Sampling rate: {MULTIPLAYER_OTLP_SPAN_RATIO}")


def instrument_django():
    DjangoInstrumentor().instrument()
    print("Django app instrumented with OpenTelemetry")
    
    # Test span creation to verify instrumentation is working
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("test_span") as span:
        span.set_attribute("test.attribute", "test_value")
        print(f"Test span created: {span}")
        print(f"Test span type: {type(span)}")
        print(f"Test span is recording: {span.is_recording()}")
