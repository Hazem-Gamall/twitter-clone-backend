import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

django_asgi_app = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from .channelsmiddleware import JwtAuthMiddlewareStack

# Would be useful if i was using session. Maybe switch to a session ws?
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
