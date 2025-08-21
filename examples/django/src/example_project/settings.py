"""
Django settings for example_project.

This example demonstrates how to use the multiplayer-session-recorder
Django middleware to capture request and response payloads.
"""

import os
import sys
from pathlib import Path

# Add the library source to Python path for local development
# This allows us to use the middleware directly from source without publishing the library
library_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'src'))
sys.path.insert(0, library_src_path)
print(f"Using middleware from: {library_src_path}")

# Import config for PORT and other settings
from config import PORT, API_PREFIX

# Initialize OpenTelemetry
import otel
otel.init_opentelemetry()
otel.instrument_django()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-example-key-for-demo-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',  # Our example API app
]

MIDDLEWARE = [
    # Add the multiplayer session recorder middleware early in the stack
    'multiplayer_session_recorder.middleware.django_http_payload_recorder.DjangoOtelHttpPayloadRecorderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'example_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Server configuration from config.py
# PORT is used when running the server: python manage.py runserver 0.0.0.0:PORT

# Multiplayer Session Recorder Middleware Configuration
MULTIPLAYER_MIDDLEWARE_CONFIG = {
    'captureBody': True,           # Capture request/response bodies
    'captureHeaders': True,        # Capture request/response headers
    'maxPayloadSizeBytes': 10000,  # Maximum payload size to capture
    'isMaskBodyEnabled': True,     # Enable masking of sensitive body fields
    'maskBodyFieldsList': ["password", "token", "secret", "api_key"],  # Fields to mask
    'isMaskHeadersEnabled': True,  # Enable masking of sensitive headers
    'maskHeadersList': ["authorization", "x-api-key", "cookie"],       # Headers to mask
}
