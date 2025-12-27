"""
Django benchmark application.

Minimal ASGI app returning JSON payload for benchmarking.
Run with: gunicorn -w 4 -b 127.0.0.1:8002 django_app:application

This is a minimal Django setup without a full project structure.
"""


import django
from django.conf import settings
from django.http import JsonResponse
from django.urls import path

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY='benchmark-secret-key-not-for-production',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        MIDDLEWARE=[],
    )
    django.setup()

# Standard response payload
RESPONSE_DATA = {
    'status': 'ok',
    'message': 'Hello from Django',
    'data': {
        'id': 12345,
        'username': 'alice_dev',
        'email': 'alice@example.com',
    },
}


def index(request):
    """Root endpoint returning JSON."""
    return JsonResponse(RESPONSE_DATA)


def health(request):
    """Health check endpoint."""
    return JsonResponse({'status': 'healthy'})


# URL patterns
urlpatterns = [
    path('', index),
    path('health', health),
]

# WSGI application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8002', '--noreload'])
