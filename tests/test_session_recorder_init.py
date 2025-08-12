#!/usr/bin/env python3
"""
Test script to verify that the session_recorder.init method works correctly
with the provided example configuration.
"""

import sys
import os
from unittest.mock import Mock, patch

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_session_recorder_init_with_example_config():
    """Test that session_recorder.init works with the provided example configuration."""
    try:
        from multiplayer_session_recorder import session_recorder
        from multiplayer_session_recorder.trace.id_generator import SessionRecorderRandomIdGenerator
        
        # Mock environment variables and constants
        MULTIPLAYER_OTLP_KEY = "test-api-key-12345"
        SERVICE_NAME = "test-service"
        SERVICE_VERSION = "1.0.0"
        PLATFORM_ENV = "development"
        
        # Create a mock trace ID generator
        otel = SessionRecorderRandomIdGenerator()
        
        # Test the init method with the exact example provided
        session_recorder.init(
            apiKey=MULTIPLAYER_OTLP_KEY,
            traceIdGenerator=otel,
            resourceAttributes={
                "serviceName": SERVICE_NAME,
                "version": SERVICE_VERSION,
                "environment": PLATFORM_ENV,
            }
        )
        
        print("✓ session_recorder.init() worked correctly with example configuration")
        
        # Verify that the session recorder is initialized
        assert session_recorder._is_initialized is True
        assert session_recorder._resource_attributes["serviceName"] == SERVICE_NAME
        assert session_recorder._resource_attributes["version"] == SERVICE_VERSION
        assert session_recorder._resource_attributes["environment"] == PLATFORM_ENV
        assert session_recorder._trace_id_generator == otel
        
        print("✓ All attributes were set correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in session_recorder.init() test: {e}")
        return False


def test_session_recorder_init_with_dict_config():
    """Test that session_recorder.init works with dictionary configuration."""
    try:
        from multiplayer_session_recorder import session_recorder
        from multiplayer_session_recorder.trace.id_generator import SessionRecorderRandomIdGenerator
        
        # Create a new session recorder instance for this test
        test_recorder = type(session_recorder)()
        
        # Test with dictionary config
        config_dict = {
            "apiKey": "test-api-key",
            "traceIdGenerator": SessionRecorderRandomIdGenerator(),
            "resourceAttributes": {
                "serviceName": "test-service",
                "version": "1.0.0",
                "environment": "test"
            }
        }
        
        test_recorder.init(config_dict)
        
        print("✓ session_recorder.init() worked correctly with dictionary configuration")
        
        # Verify initialization
        assert test_recorder._is_initialized is True
        assert test_recorder._resource_attributes["serviceName"] == "test-service"
        
        return True
        
    except Exception as e:
        print(f"✗ Error in dictionary config test: {e}")
        return False


def test_session_recorder_init_with_keyword_args():
    """Test that session_recorder.init works with keyword arguments."""
    try:
        from multiplayer_session_recorder import session_recorder
        from multiplayer_session_recorder.trace.id_generator import SessionRecorderRandomIdGenerator
        
        # Create a new session recorder instance for this test
        test_recorder = type(session_recorder)()
        
        # Test with keyword arguments
        test_recorder.init(
            apiKey="test-api-key",
            traceIdGenerator=SessionRecorderRandomIdGenerator(),
            resourceAttributes={
                "serviceName": "test-service",
                "version": "1.0.0"
            }
        )
        
        print("✓ session_recorder.init() worked correctly with keyword arguments")
        
        # Verify initialization
        assert test_recorder._is_initialized is True
        assert test_recorder._resource_attributes["serviceName"] == "test-service"
        
        return True
        
    except Exception as e:
        print(f"✗ Error in keyword args test: {e}")
        return False


def test_session_recorder_init_validation():
    """Test that session_recorder.init properly validates input."""
    try:
        from multiplayer_session_recorder import session_recorder
        
        # Create a new session recorder instance for this test
        test_recorder = type(session_recorder)()
        
        # Test missing apiKey
        try:
            test_recorder.init(
                apiKey="",  # Empty string
                traceIdGenerator=Mock(),
                resourceAttributes={}
            )
            print("✗ Expected ValueError for empty apiKey but no exception was raised")
            return False
        except ValueError as e:
            if "Api key not provided" in str(e):
                print("✓ Correctly raised ValueError for empty apiKey")
            else:
                print(f"✗ Unexpected error message: {e}")
                return False
        
        # Test missing traceIdGenerator
        try:
            test_recorder.init(
                apiKey="test-key",
                traceIdGenerator=None,
                resourceAttributes={}
            )
            print("✗ Expected ValueError for None traceIdGenerator but no exception was raised")
            return False
        except ValueError as e:
            if "Incompatible trace id generator" in str(e):
                print("✓ Correctly raised ValueError for None traceIdGenerator")
            else:
                print(f"✗ Unexpected error message: {e}")
                return False
        
        print("✓ session_recorder.init() validation works correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in validation test: {e}")
        return False


def test_session_recorder_init_with_none_resource_attributes():
    """Test that session_recorder.init works when resourceAttributes is None."""
    try:
        from multiplayer_session_recorder import session_recorder
        from multiplayer_session_recorder.trace.id_generator import SessionRecorderRandomIdGenerator
        
        # Create a new session recorder instance for this test
        test_recorder = type(session_recorder)()
        
        # Test with None resourceAttributes
        test_recorder.init(
            apiKey="test-api-key",
            traceIdGenerator=SessionRecorderRandomIdGenerator(),
            resourceAttributes=None
        )
        
        print("✓ session_recorder.init() worked correctly with None resourceAttributes")
        
        # Verify that resource_attributes is an empty dict when None is passed
        assert test_recorder._is_initialized is True
        assert test_recorder._resource_attributes == {}
        
        return True
        
    except Exception as e:
        print(f"✗ Error in None resourceAttributes test: {e}")
        return False


if __name__ == "__main__":
    print("Testing session_recorder.init() method...")
    print("=" * 50)
    
    success = True
    
    success &= test_session_recorder_init_with_example_config()
    print()
    
    success &= test_session_recorder_init_with_dict_config()
    print()
    
    success &= test_session_recorder_init_with_keyword_args()
    print()
    
    success &= test_session_recorder_init_validation()
    print()
    
    success &= test_session_recorder_init_with_none_resource_attributes()
    print()
    
    if success:
        print("🎉 All tests passed! The session_recorder.init() method works correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1) 