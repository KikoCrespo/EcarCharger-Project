"""
ASGI config for APIRest project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set DJANGO_SETTINGS_MODULE first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "APIRest.settings")

# Initialize Django application BEFORE importing consumers/routing
django_asgi_app = get_asgi_application()

# Now import other dependencies that require Django to be initialized
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from APIRest import routing  # This imports consumers.py AFTER Django setup

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
    )
})