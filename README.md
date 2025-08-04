Session Recorder python
============================================================================
##  Introduction
The multiplayer-session-recorder module integrates OpenTelemetry with the Multiplayer platform to enable seamless trace collection and analysis. This library helps developers monitor, debug, and document application performance with detailed trace data. It supports flexible trace ID generation, sampling strategies.

## Installation

To install the `multiplayer-session-recorder` module, use the following command:

```bash
pip install multiplayer-session-recorder
```

## Session Recorder Initialization

```python
from multiplayer.session_recorder import session_recorder

session_recorder.init({
  apiKey: "{YOUR_API_KEY}",
  traceIdGenerator: idGenerator,
  resourceAttributes: {
    serviceName: "{YOUR_APPLICATION_NAME}",
    version: "{YOUR_APPLICATION_VERSION}",
    environment: "{YOUR_APPLICATION_ENVIRONMENT}",
  }
})
```

## Example Usage

```python
from multiplayer.session_recorder import session_recorder, SessionType
// Session recorder trace id generator which is used during opentelemetry initialization
from .opentelemetry import id_generator

session_recorder.init({
  apiKey: "{YOUR_API_KEY}",
  traceIdGenerator: id_generator,
  resourceAttributes: {
    serviceName: "{YOUR_APPLICATION_NAME}",
    version: "{YOUR_APPLICATION_VERSION}",
    environment: "{YOUR_APPLICATION_ENVIRONMENT}",
  }
})

// ...

session_recorder.start(
    SessionType.PLAIN,
    {
      name: 'This is test session',
      sessionAttributes: {
        accountId: '687e2c0d3ec8ef6053e9dc97',
        accountName: 'Acme Corporation'
      }
    }
  )

  // do something here

  session_recorder.stop()
```

## Session Recorder trace Id generator

```python
from multiplayer.session_recorder import SessionRecorderTraceIdRatioBasedSampler

sampler = SessionRecorderTraceIdRatioBasedSampler(rate = 1/2)
```

## Session Recorder trace id ratio based sampler

```python
from multiplayer.session_recorder import SessionRecorderRandomIdGenerator

id_generator = SessionRecorderRandomIdGenerator(autoDocTracesRatio = 1/1000)
```

## Django http payload recorder middleware

```python
from multiplayer.session_recorder import DjangoOtelHttpPayloadRecorderMiddleware

DjangoOtelHttpPayloadRecorderMiddleware({
    "captureBody": True,
    "captureHeaders": True,
    "maxPayloadSizeBytes": 10000,
    "isMaskBodyEnabled": True,
    "maskBodyFieldsList": ["password", "token"],
    "isMaskHeadersEnabled": True,
    "maskHeadersList": ["authorization"],
})

```

## Flask http payload recorder middleware

```python
from flask import Flask
from multiplayer.session_recorder import FlaskOtelHttpPayloadRecorderMiddleware

app = Flask(__name__)

# Add middleware BEFORE request handlers run
@app.before_request
def before_request():
    FlaskOtelHttpPayloadRecorderMiddleware.capture_request_body(
        maxPayloadSizeBytes=10000,
        captureBody=True,
        captureHeaders=True,
        isMaskBodyEnabled=True,
        maskBodyFieldsList=["password", "secret"],
        isMaskHeadersEnabled=True,
        maskHeadersList=["authorization"],
    )

# Add middleware AFTER request finishes
@app.after_request
def after_request(response):
    FlaskOtelHttpPayloadRecorderMiddleware.capture_response_body(
        response,
        maxPayloadSizeBytes=10000,
        captureBody=True,
        captureHeaders=True,
        isMaskBodyEnabled=True,
        maskBodyFieldsList=["token"],
        isMaskHeadersEnabled=True,
        maskHeadersList=["set-cookie"],
    )
    return response
```
