"""
Django API views demonstrating HTTP payload recording.

These views show how the multiplayer-session-recorder middleware
captures and masks request/response payloads.
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def hello(request):
    """Simple hello endpoint."""
    return JsonResponse({
        "message": "Hello from Django with payload recording!",
        "status": "success"
    })


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Login endpoint that will have sensitive data masked."""
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')  # This will be masked in captured payload
        
        return JsonResponse({
            "message": "Login processed",
            "user": username,
            "status": "authenticated"
        })
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)


@require_http_methods(["GET", "POST"])
def handle_data(request):
    """Endpoint that handles both GET and POST requests."""
    if request.method == 'GET':
        return JsonResponse({
            "method": "GET",
            "data": "Sample data from GET request",
            "headers": dict(request.headers)
        })
    else:
        try:
            data = json.loads(request.body)
            return JsonResponse({
                "method": "POST",
                "received_data": data,
                "status": "processed"
            })
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def sensitive_endpoint(request):
    """Endpoint with sensitive data that will be masked."""
    try:
        data = json.loads(request.body)
        
        # These fields will be masked in the captured payload
        sensitive_info = {
            "api_key": data.get('api_key', ''),
            "secret_token": data.get('secret_token', ''),
            "password": data.get('password', ''),
            "public_data": data.get('public_data', 'This will not be masked')
        }
        
        return JsonResponse({
            "message": "Sensitive data processed",
            "public_data": sensitive_info["public_data"],
            "status": "success"
        })
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)
