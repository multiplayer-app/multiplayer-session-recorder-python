"""
Middleware factory for Django and Flask HTTP payload recording.

This module provides factory functions that create middleware instances
for capturing HTTP request/response payloads and adding them to OpenTelemetry attributes.

Usage:
    # For Django
    from multiplayer_session_recorder.middleware import create_django_middleware
    MIDDLEWARE = [
        'your_app.middleware.CustomMiddleware',
        create_django_middleware(),
        # ... other middleware
    ]

    # For Flask
    from multiplayer_session_recorder.middleware import create_flask_middleware
    app = Flask(__name__)
    before_request, after_request = create_flask_middleware()
    app.before_request(before_request)
    app.after_request(after_request)
"""

from typing import Optional, Tuple, Callable, Any
from ..types.middleware_config import HttpMiddlewareConfig


def create_django_middleware(config: Optional[HttpMiddlewareConfig] = None):
    """
    Create a Django middleware class for HTTP payload recording.
    
    Args:
        config: Optional configuration for the middleware
        
    Returns:
        Django middleware class
        
    Raises:
        ImportError: If Django is not installed
    """
    try:
        from .django_http_payload_recorder import DjangoOtelHttpPayloadRecorderMiddleware
        return DjangoOtelHttpPayloadRecorderMiddleware(config=config)
    except ImportError as e:
        if "django" in str(e).lower():
            raise ImportError(
                "Django is required for Django middleware. "
                "Install it with: pip install multiplayer-session-recorder[django]"
            ) from e
        raise


def create_flask_middleware(config: Optional[HttpMiddlewareConfig] = None) -> Tuple[Callable, Callable]:
    """
    Create Flask middleware functions for HTTP payload recording.
    
    Args:
        config: Optional configuration for the middleware
        
    Returns:
        Tuple of (before_request, after_request) functions
        
    Raises:
        ImportError: If Flask is not installed
    """
    try:
        from .flask_http_payload_recorder import FlaskOtelHttpPayloadRecorderMiddleware
        return FlaskOtelHttpPayloadRecorderMiddleware(config)
    except ImportError as e:
        if "flask" in str(e).lower():
            raise ImportError(
                "Flask is required for Flask middleware. "
                "Install it with: pip install multiplayer-session-recorder[flask]"
            ) from e
        raise


def is_django_available() -> bool:
    """Check if Django is available for import."""
    try:
        import django
        return True
    except ImportError:
        return False


def is_flask_available() -> bool:
    """Check if Flask is available for import."""
    try:
        import flask
        return True
    except ImportError:
        return False


# Convenience imports for direct access
try:
    from .django_http_payload_recorder import DjangoOtelHttpPayloadRecorderMiddleware
    __all__ = [
        'DjangoOtelHttpPayloadRecorderMiddleware',
        'create_django_middleware',
        'create_flask_middleware',
        'is_django_available',
        'is_flask_available'
    ]
except ImportError:
    __all__ = [
        'create_django_middleware',
        'create_flask_middleware', 
        'is_django_available',
        'is_flask_available'
    ] 