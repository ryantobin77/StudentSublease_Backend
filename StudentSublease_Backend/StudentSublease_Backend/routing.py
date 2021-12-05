from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import messaging.routing
from django.core.asgi import get_asgi_application


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # (http->django views is added by default)
    'websocket': URLRouter(
        messaging.routing.websocket_urlpatterns
    )
})

