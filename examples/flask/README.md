# Flask HTTP Payload Recorder Example

This example demonstrates how to use the `multiplayer-session-recorder` Flask middleware to capture and mask HTTP request/response payloads.

## Features Demonstrated

- **Request/Response Body Capture**: Captures JSON and text payloads
- **Header Capture**: Captures request and response headers
- **Sensitive Data Masking**: Automatically masks passwords, tokens, and other sensitive fields
- **Payload Size Limiting**: Configurable maximum payload size
- **Selective Header Filtering**: Include/exclude specific headers
- **OpenTelemetry Integration**: Automatic instrumentation with console exporter for demo

## Installation

```bash
pip install -r requirements.txt
```

**Note**: This example uses the middleware directly from the library source code without requiring the library to be published. The app imports the middleware classes directly from the `src/` directory.

## Usage

1. **Start the Flask application**:
   ```bash
   python src/app.py
   ```

2. **Test the endpoints**:

   **Hello endpoint**:
   ```bash
   curl http://localhost:3000/
   ```

   **Login with sensitive data** (password will be masked):
   ```bash
   curl -X POST http://localhost:3000/api/v1/login \
     -H "Content-Type: application/json" \
     -d '{"username": "john", "password": "secret123"}'
   ```

   **Sensitive data endpoint** (api_key, secret_token, password will be masked):
   ```bash
   curl -X POST http://localhost:3000/api/v1/sensitive \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer secret-token" \
     -d '{"api_key": "sk-123456", "secret_token": "xyz789", "password": "mypass", "public_data": "visible"}'
   ```

   **Data endpoint with headers**:
   ```bash
   curl -X POST http://localhost:3000/api/v1/data \
     -H "Content-Type: application/json" \
     -H "X-Custom-Header: test-value" \
     -d '{"message": "test data"}'
   ```

   **GET data endpoint**:
   ```bash
   curl http://localhost:3000/api/v1/data
   ```

## Configuration

The middleware is configured in `app.py`:

```python
middleware_config = HttpMiddlewareConfig(
    captureBody=True,           # Capture request/response bodies
    captureHeaders=True,        # Capture request/response headers
    maxPayloadSizeBytes=10000,  # Maximum payload size to capture
    isMaskBodyEnabled=True,     # Enable masking of sensitive body fields
    maskBodyFieldsList=["password", "token", "secret", "api_key"],  # Fields to mask
    isMaskHeadersEnabled=True,  # Enable masking of sensitive headers
    maskHeadersList=["authorization", "x-api-key", "cookie"],       # Headers to mask
)
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

The example includes OpenTelemetry initialization with a console exporter, so you can see traces directly in the console output.

The captured payloads are automatically added to OpenTelemetry spans as attributes:
- `multiplayer.http.request.body`
- `multiplayer.http.request.headers`
- `multiplayer.http.response.body`
- `multiplayer.http.response.headers`

When you run the Flask app and make requests, you'll see detailed trace information in the console, including:
- HTTP request/response spans
- Captured and masked payloads
- Request/response headers
- Timing information

Example console output:
```
{
  "name": "GET /api/data",
  "context": {...},
  "attributes": {
    "multiplayer.http.request.headers": "{'Host': 'localhost:5000', 'User-Agent': 'curl/7.68.0'}",
    "multiplayer.http.response.headers": "{'Content-Type': 'application/json'}",
    "http.method": "GET",
    "http.url": "http://localhost:5000/api/data",
    "http.status_code": 200
  }
}
```
