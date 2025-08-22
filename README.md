![Description](.github/header-python.png)

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

# Multiplayer Session Recorder - Python

## Introduction

The `multiplayer-session-recorder` module integrates OpenTelemetry with the Multiplayer platform to enable seamless trace collection and analysis. This library helps developers monitor, debug, and document application performance with detailed trace data. It supports flexible trace ID generation, sampling strategies.

## Installation

To install the `multiplayer-session-recorder` module, use the following command:

```bash
pip install multiplayer-session-recorder
```

### Optional Dependencies

The library supports optional dependencies for web framework integrations:

```bash
# For Django support
pip install multiplayer-session-recorder[django]

# For Flask support
pip install multiplayer-session-recorder[flask]

# For both Django and Flask support
pip install multiplayer-session-recorder[all]
```

## Session Recorder Initialization

```python
from multiplayer_session_recorder import session_recorder

session_recorder.init(
  apiKey = "{YOUR_API_KEY}",
  traceIdGenerator = idGenerator,
  resourceAttributes = {
    "serviceName": SERVICE_NAME,
    "version": SERVICE_VERSION,
    "environment": PLATFORM_ENV,
  }
)
```

## Example Usage

```python
from multiplayer_session_recorder import session_recorder, SessionType
// Session recorder trace id generator which is used during opentelemetry initialization
from .opentelemetry import id_generator

session_recorder.init(
  apiKey = "{YOUR_API_KEY}",
  traceIdGenerator = idGenerator,
  resourceAttributes = {
    "serviceName": SERVICE_NAME,
    "version": SERVICE_VERSION,
    "environment": PLATFORM_ENV,
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

## Session Recorder trace Id generator

```python
from multiplayer_session_recorder import SessionRecorderTraceIdRatioBasedSampler

sampler = SessionRecorderTraceIdRatioBasedSampler(rate = 1/2)
```

## Session Recorder trace id ratio based sampler

```python
from multiplayer_session_recorder import SessionRecorderRandomIdGenerator

id_generator = SessionRecorderRandomIdGenerator(autoDocTracesRatio = 1/1000)
```

## Django HTTP Payload Recorder Middleware

First, install Django support:

```bash
pip install multiplayer-session-recorder[django]
```

Then use the middleware in your Django settings:

```python
from multiplayer_session_recorder import create_django_middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

## Flask HTTP Payload Recorder Middleware

First, install Flask support:

```bash
pip install multiplayer-session-recorder[flask]
```

Then use the middleware in your Flask application:

```python
from flask import Flask
from multiplayer_session_recorder import create_flask_middleware

app = Flask(__name__)

# Create middleware functions
before_request, after_request = create_flask_middleware({
    "captureBody": True,
    "captureHeaders": True,
    "maxPayloadSizeBytes": 10000,
    "isMaskBodyEnabled": True,
    "maskBodyFieldsList": ["password", "secret"],
    "isMaskHeadersEnabled": True,
    "maskHeadersList": ["authorization"],
})

# Register the middleware
app.before_request(before_request)
app.after_request(after_request)

@app.route('/')
def hello():
    return 'Hello, World!'
```
