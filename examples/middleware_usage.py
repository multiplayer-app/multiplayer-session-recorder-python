#!/usr/bin/env python3
"""
Example usage of the multiplayer session recorder middleware with optional dependencies.

This script demonstrates how to use the middleware with Django and Flask,
showing both the factory functions and direct class usage.
"""

from multiplayer_session_recorder import (
    create_django_middleware,
    create_flask_middleware,
    is_django_available,
    is_flask_available,
    HttpMiddlewareConfig
)

def main():
    print("Multiplayer Session Recorder Middleware Examples")
    print("=" * 50)
    
    # Check availability
    print(f"Django available: {is_django_available()}")
    print(f"Flask available: {is_flask_available()}")
    print()
    
    # Example configuration
    config = HttpMiddlewareConfig(
        captureBody=True,
        captureHeaders=True,
        maxPayloadSizeBytes=10000,
        isMaskBodyEnabled=True,
        maskBodyFieldsList=["password", "token", "secret"],
        isMaskHeadersEnabled=True,
        maskHeadersList=["authorization", "x-api-key"]
    )
    
    # Django example
    if is_django_available():
        print("Django Middleware Example:")
        print("-" * 30)
        try:
            django_middleware = create_django_middleware(config)
            print("✓ Django middleware created successfully")
            print(f"  Class: {django_middleware.__class__.__name__}")
        except Exception as e:
            print(f"✗ Failed to create Django middleware: {e}")
        print()
    else:
        print("Django not available. Install with: pip install multiplayer-session-recorder[django]")
        print()
    
    # Flask example
    if is_flask_available():
        print("Flask Middleware Example:")
        print("-" * 30)
        try:
            before_request, after_request = create_flask_middleware(config)
            print("✓ Flask middleware created successfully")
            print(f"  before_request: {before_request.__name__}")
            print(f"  after_request: {after_request.__name__}")
        except Exception as e:
            print(f"✗ Failed to create Flask middleware: {e}")
        print()
    else:
        print("Flask not available. Install with: pip install multiplayer-session-recorder[flask]")
        print()
    
    print("Installation commands:")
    print("  pip install multiplayer-session-recorder[django]  # For Django")
    print("  pip install multiplayer-session-recorder[flask]   # For Flask")
    print("  pip install multiplayer-session-recorder[all]     # For both")

if __name__ == "__main__":
    main() 