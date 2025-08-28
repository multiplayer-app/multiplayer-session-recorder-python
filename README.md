![Description](./docs/img/header-python.png)

<div align="center">
<a href="https://github.com/multiplayer-app/multiplayer-session-recorder-python">
  <img src="https://img.shields.io/github/stars/multiplayer-app/multiplayer-session-recorder-python.svg?style=social&label=Star&maxAge=2592000" alt="GitHub stars">
</a>
  <a href="https://github.com/multiplayer-app/multiplayer-session-recorder-python/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/multiplayer-app/multiplayer-session-recorder-python" alt="License">
  </a>
  <a href="https://multiplayer.app">
    <img src="https://img.shields.io/badge/Visit-multiplayer.app-blue" alt="Visit Multiplayer">
  </a>
  
</div>
<div>
  <p align="center">
    <a href="https://x.com/trymultiplayer">
      <img src="https://img.shields.io/badge/Follow%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" />
    </a>
    <a href="https://www.linkedin.com/company/multiplayer-app/">
      <img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow on LinkedIn" />
    </a>
    <a href="https://discord.com/invite/q9K3mDzfrx">
      <img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Join our Discord" />
    </a>
  </p>
</div>

# Multiplayer Full Stack Session Recorder

## Introduction

The Multiplayer Full Stack Session Recorder is a powerful tool that offers deep session replays with insights spanning frontend screens, platform traces, metrics, and logs. It helps your team pinpoint and resolve bugs faster by providing a complete picture of your backend system architecture. No more wasted hours combing through APM data; the Multiplayer Full Stack Session Recorder does it all in one place.


## Install

```bash
pip install multiplayer-session-recorder

# For Django support
pip install multiplayer-session-recorder[django]

# For Flask support
pip install multiplayer-session-recorder[flask]
```

## Set up backend services

### Route traces and logs to Multiplayer

Multiplayer Full Stack Session Recorder is built on top of OpenTelemetry.

### New to OpenTelemetry?

No problem. You can set it up in a few minutes. If your services don't already use OpenTelemetry, you'll first need to install the OpenTelemetry libraries. Detailed instructions for this can be found in the [OpenTelemetry documentation](https://opentelemetry.io/docs/).

### Already using OpenTelemetry?

You have two primary options for routing your data to Multiplayer:

***Direct Exporter***: This option involves using the Multiplayer Exporter directly within your services. It's a great choice for new applications or startups because it's simple to set up and doesn't require any additional infrastructure. You can configure it to send all session recording data to Multiplayer while optionally sending a sampled subset of data to your existing observability platform.

***OpenTelemetry Collector***: For large, scaled platforms, we recommend using an OpenTelemetry Collector. This approach provides more flexibility by having your services send all telemetry to the collector, which then routes specific session recording data to Multiplayer and other data to your existing observability tools.


### Option 1: Direct Exporter

Send OpenTelemetry data from your services to Multiplayer and optionally other destinations (e.g., OpenTelemetry Collectors, observability platforms, etc.).

This is the quickest way to get started, but consider using an OpenTelemetry Collector (see [Option 2](#option-2-opentelemetry-collector) below) if you're scalling or a have a large platform.

```python
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from multiplayer_session_recorder.exporter.span_wrapper import OTLPSpanExporterWrapper
from multiplayer_session_recorder.exporter.log_wrapper import OTLPLogExporterWrapper
from multiplayer_session_recorder.exporter.http.trace_exporter import (
    OTLPSpanExporter as SessionRecorderOTLPSpanExporter
)
from multiplayer_session_recorder.exporter.http.log_exporter import (
    OTLPLogExporter as SessionRecorderOTLPLogExporter
)

# set up Multiplayer exporters. Note: GRPC exporters are also available.
# see: `SessionRecorderGrpcTraceExporter` and `SessionRecorderGrpcLogsExporter`
traceExporter = SessionRecorderOTLPSpanExporter(
    api_key = "MULTIPLAYER_OTLP_KEY" # note: replace with your Multiplayer OTLP key
)
logExporter = SessionRecorderOTLPLogExporter(
    api_key = "MULTIPLAYER_OTLP_KEY" # note: replace with your Multiplayer OTLP key
)

# Multiplayer exporter wrappers filter out session recording atrtributes before passing to provided exporter
traceExporter = SessionRecorderOTLPSpanExporter(
  # add any OTLP trace exporter
  OTLPSpanExporter(
    # ...
  )
)

logExporter = SessionRecorderOTLPLogExporter(
  # add any OTLP log exporter
  OTLPLogExporter(
    # ...
  )
)
```

### Option 2: OpenTelemetry Collector

If you're scalling or a have a large platform, consider running a dedicated collector. See the Multiplayer OpenTelemetry collector [repository](https://github.com/multiplayer-app/multiplayer-otlp-collector) which shows how to configure the standard OpenTelemetry Collector to send data to Multiplayer and optional other destinations.

Add standard [OpenTelemetry code](https://opentelemetry.io/docs/languages/python/exporters/) to export OTLP data to your collector.

See a basic example below:

```python
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

traceExporter = OTLPSpanExporter(
  endpoint = "http://<OTLP_COLLECTOR_URL>/v1/traces",
)

logExporter = OTLPLogExporter(
  endpoint = "http://<OTLP_COLLECTOR_URL>/v1/logs",
)
```

### Capturing request/response and header content

In addition to sending traces and logs, you need to capture request and response content. We offer two solutions for this:

***In-Service Code Capture:*** You can use our libraries to capture, serialize, and mask request/response and header content directly within your service code. This is an easy way to get started, especially for new projects, as it requires no extra components in your platform.

***Multiplayer Proxy:*** Alternatively, you can run a [Multiplayer Proxy](https://github.com/multiplayer-app/multiplayer-proxy) to handle this outside of your services. This is ideal for large-scale applications and supports all languages, including those like Java that don't allow for in-service request/response hooks. The proxy can be deployed in various ways, such as an Ingress Proxy, a Sidecar Proxy, or an Embedded Proxy, to best fit your architecture.

### Option 1: In-Service Code Capture

The Multiplayer Session Recorder library provides utilities for capturing request, response and header content.

For Django see example below:

```python
from multiplayer_session_recorder import create_django_middleware

MIDDLEWARE = [
    # ...
    'multiplayer_session_recorder.middleware.django_http_payload_recorder.DjangoOtelHttpPayloadRecorderMiddleware',
    # Add the payload recorder middleware
    create_django_middleware({
        "captureBody": True,
        "captureHeaders": True,
        "maxPayloadSizeBytes": 10000,
        "isMaskBodyEnabled": True,
        "maskBodyFieldsList": ["password", "token"],
        "isMaskHeadersEnabled": True,
        "maskHeadersList": ["authorization"],
    }),
]
```

For Django see example below:

```python
from flask import Flask
from multiplayer_session_recorder.middleware.flask_http_payload_recorder import FlaskOtelHttpPayloadRecorderMiddleware
from multiplayer_session_recorder.types.middleware_config import HttpMiddlewareConfig

app = Flask(__name__)

# Create middleware functions
middleware_config = HttpMiddlewareConfig(
  # capture request/response content
  captureBody=True
  # capture request/response headers
  captureHeaders=True,
  # set the maximum request/response content size (in bytes) that will be captured
  # any request/response content greater than size will be not included in session recordings
  maxPayloadSizeBytes=10000,
  # enable masking of sensitive body fields
  isMaskBodyEnabled=True,
  # list of field names to mask in request/response content
  maskBodyFieldsList=["password", "token", "secret", "api_key"],
  # enable masking of sensitive headers
  isMaskHeadersEnabled=True,
  # list of headers to mask in request/response headers
  maskHeadersList=["authorization", "x-api-key", "cookie"]
)

# create middleware functions using the direct middleware class
before_request, after_request = FlaskOtelHttpPayloadRecorderMiddleware(middleware_config)

# register the middleware
app.before_request(before_request)
app.after_request(after_request)

@app.route('/')
def hello():
    return 'Hello, World!'
```

### Option 2: Multiplayer Proxy

The Multiplayer Proxy enables capturing request/response and header content without changing service code. See instructions at the [Multiplayer Proxy repository](https://github.com/multiplayer-app/multiplayer-proxy).

## Set up CLI app

The Multiplayer Full Stack Session Recorder can be used inside the CLI apps.

The [Multiplayer Time Travel Demo](https://github.com/multiplayer-app/multiplayer-time-travel-platform) includes an example [python CLI app](https://github.com/multiplayer-app/multiplayer-time-travel-platform/tree/main/clients/python-cli-app).

See an additional example below.

### Quick start

Use the following code below to initialize and run the session recorder.

```python
# IMPORTANT: set up OpenTelemetry
# for an example see ./examples/cli/src/otel.py
# NOTE: for the code below to work, copy ./examples/cli/src/otel.py to ./otel.py
import otel

otel.init_tracing()

from multiplayer_session_recorder import (
  session_recorder,
  SessionType,
  SessionRecorderRandomIdGenerator
)

session_recorder.init(
  apiKey = "MULTIPLAYER_OTLP_KEY", // note: replace with your Multiplayer OTLP key
  traceIdGenerator = otel.id_generator,
  resourceAttributes = {
    "serviceName": "{YOUR_APPLICATION_NAME}"
    "version": "{YOUR_APPLICATION_VERSION}",
    "environment": "{YOUR_APPLICATION_ENVIRONMENT}",
  }
)

# ...

await session_recorder.start(
    SessionType.PLAIN,
    {
      name: "This is test session",
      sessionAttributes: {
        accountId: "687e2c0d3ec8ef6053e9dc97",
        accountName: "Acme Corporation"
      }
    }
  )

  # do something here

await session_recorder.stop()
```

Replace the placeholders with your application’s version, name, environment, and API key.

## License

MIT — see [LICENSE](./LICENSE).
