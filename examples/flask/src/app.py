#!/usr/bin/env python3
from flask import Flask, request, jsonify
import sys
import os

# Add the library source to Python path for local development
# This allows us to use the middleware directly from source without publishing the library
library_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
sys.path.insert(0, library_src_path)
print(f"Using middleware from: {library_src_path}")

from multiplayer_session_recorder.middleware.flask_http_payload_recorder import FlaskOtelHttpPayloadRecorderMiddleware
from multiplayer_session_recorder.types.middleware_config import HttpMiddlewareConfig

# Verify we're using the source code version
print(f"Middleware module location: {FlaskOtelHttpPayloadRecorderMiddleware.__module__}")

# OpenTelemetry initialization
from otel import init_opentelemetry, instrument_flask
from config import PORT, API_PREFIX

# Create Flask app
app = Flask(__name__)

# Initialize OpenTelemetry before creating the app
init_opentelemetry()

# Instrument Flask with OpenTelemetry
instrument_flask(app)

# Configure the middleware
middleware_config = HttpMiddlewareConfig(
    captureBody=True,           # Capture request/response bodies
    captureHeaders=True,        # Capture request/response headers
    maxPayloadSizeBytes=10000,  # Maximum payload size to capture
    isMaskBodyEnabled=True,     # Enable masking of sensitive body fields
    maskBodyFieldsList=["password", "token", "secret", "api_key"],  # Fields to mask
    isMaskHeadersEnabled=True,  # Enable masking of sensitive headers
    maskHeadersList=["authorization", "x-api-key", "cookie"],       # Headers to mask
)

# Create middleware functions using the direct middleware class
before_request, after_request = FlaskOtelHttpPayloadRecorderMiddleware(middleware_config)

# Register the middleware
app.before_request(before_request)
app.after_request(after_request)

@app.route('/')
def hello():
    """Simple hello endpoint"""
    return jsonify({
        "message": "Hello from Flask with payload recording!",
        "status": "success"
    })

@app.route(f'{API_PREFIX}/login', methods=['POST'])
def login():
    """Login endpoint that will have sensitive data masked"""
    data = request.get_json()
    
    # This password will be masked in the captured payload
    password = data.get('password', '')
    username = data.get('username', '')
    
    return jsonify({
        "message": "Login processed",
        "user": username,
        "status": "authenticated"
    })

@app.route(f'{API_PREFIX}/data', methods=['GET', 'POST'])
def handle_data():
    """Endpoint that handles both GET and POST requests"""
    if request.method == 'GET':
        return jsonify({
            "method": "GET",
            "data": "Sample data from GET request",
            "headers": dict(request.headers)
        })
    else:
        data = request.get_json()
        return jsonify({
            "method": "POST",
            "received_data": data,
            "status": "processed"
        })

@app.route(f'{API_PREFIX}/sensitive', methods=['POST'])
def sensitive_endpoint():
    """Endpoint with sensitive data that will be masked"""
    data = request.get_json()
    
    # These fields will be masked in the captured payload
    sensitive_info = {
        "api_key": data.get('api_key', ''),
        "secret_token": data.get('secret_token', ''),
        "password": data.get('password', ''),
        "public_data": data.get('public_data', 'This will not be masked')
    }
    
    return jsonify({
        "message": "Sensitive data processed",
        "public_data": sensitive_info["public_data"],
        "status": "success"
    })

if __name__ == '__main__':
    print("Flask HTTP Payload Recorder Example")
    print("=" * 40)
    print("The middleware will capture and mask sensitive data in requests/responses.")
    print("Check your OpenTelemetry traces to see the captured payloads.")
    print()
    print("Available endpoints:")
    print("  GET  /                    - Hello message")
    print(f"  POST {API_PREFIX}/login           - Login with password masking")
    print(f"  GET  {API_PREFIX}/data            - Get data with headers")
    print(f"  POST {API_PREFIX}/data            - Post data")
    print(f"  POST {API_PREFIX}/sensitive       - Sensitive data with masking")
    print()
    print(f"Starting server on http://localhost:{PORT}")
    app.run(debug=True, host='0.0.0.0', port=PORT)
