# Django HTTP Payload Recorder Example

This example demonstrates how to use the `multiplayer-session-recorder` Django middleware to capture and mask HTTP request/response payloads.

## Features Demonstrated

- **Request/Response Body Capture**: Captures JSON and text payloads
- **Header Capture**: Captures request and response headers
- **Sensitive Data Masking**: Automatically masks passwords, tokens, and other sensitive fields
- **Payload Size Limiting**: Configurable maximum payload size
- **Selective Header Filtering**: Include/exclude specific headers

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. **Run Django migrations** (creates the database):
   ```bash
   python manage.py migrate
   ```

2. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

3. **Test the endpoints**:

   **Hello endpoint**:
   ```bash
   curl http://localhost:8000/api/hello/
   ```

   **Login with sensitive data** (password will be masked):
   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "john", "password": "secret123"}'
   ```

   **Sensitive data endpoint** (api_key, secret_token, password will be masked):
   ```bash
   curl -X POST http://localhost:8000/api/sensitive/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer secret-token" \
     -d '{"api_key": "sk-123456", "secret_token": "xyz789", "password": "mypass", "public_data": "visible"}'
   ```

   **Data endpoint with headers**:
   ```bash
   curl -X POST http://localhost:8000/api/data/ \
     -H "Content-Type: application/json" \
     -H "X-Custom-Header: test-value" \
     -d '{"message": "test data"}'
   ```

## Configuration

The middleware is configured in `example_project/settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware ...
    'multiplayer_session_recorder.middleware.django_http_payload_recorder.DjangoOtelHttpPayloadRecorderMiddleware',
]

# Middleware configuration
MULTIPLAYER_MIDDLEWARE_CONFIG = {
    'captureBody': True,           # Capture request/response bodies
    'captureHeaders': True,        # Capture request/response headers
    'maxPayloadSizeBytes': 10000,  # Maximum payload size to capture
    'isMaskBodyEnabled': True,     # Enable masking of sensitive body fields
    'maskBodyFieldsList': ["password", "token", "secret", "api_key"],  # Fields to mask
    'isMaskHeadersEnabled': True,  # Enable masking of sensitive headers
    'maskHeadersList': ["authorization", "x-api-key", "cookie"],       # Headers to mask
}
```

## Alternative Configuration Method

You can also configure the middleware using the factory function:

```python
from multiplayer_session_recorder import create_django_middleware, HttpMiddlewareConfig

# In your settings.py
config = HttpMiddlewareConfig(
    captureBody=True,
    captureHeaders=True,
    maxPayloadSizeBytes=10000,
    isMaskBodyEnabled=True,
    maskBodyFieldsList=["password", "token", "secret", "api_key"],
    isMaskHeadersEnabled=True,
    maskHeadersList=["authorization", "x-api-key", "cookie"],
)

# Create middleware class
DjangoOtelHttpPayloadRecorderMiddleware = create_django_middleware(config)

# Add to MIDDLEWARE
MIDDLEWARE = [
    # ... other middleware ...
    'path.to.DjangoOtelHttpPayloadRecorderMiddleware',
]
```

## What Gets Captured

- **Request bodies**: JSON and text payloads
- **Response bodies**: JSON responses
- **Request headers**: All headers (with sensitive ones masked)
- **Response headers**: All response headers

## What Gets Masked

- **Body fields**: `password`, `token`, `secret`, `api_key`
- **Headers**: `authorization`, `x-api-key`, `cookie`

## OpenTelemetry Integration

The captured payloads are automatically added to OpenTelemetry spans as attributes:
- `multiplayer.http.request.body`
- `multiplayer.http.request.headers`
- `multiplayer.http.response.body`
- `multiplayer.http.response.headers`

Check your OpenTelemetry traces to see the captured and masked payloads.

## Project Structure

```
examples/django/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── example_project/         # Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings with middleware config
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
└── api/                     # Example API app
    ├── __init__.py
    ├── urls.py              # API URL patterns
    └── views.py             # API views with example endpoints
```
