"""URL patterns for the API app."""
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('login/', views.login, name='login'),
    path('data/', views.handle_data, name='data'),
    path('sensitive/', views.sensitive_endpoint, name='sensitive'),
]
