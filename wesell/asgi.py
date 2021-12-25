import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesell.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
import products.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            products.routing.websocket_urlpatterns
        )
    ),
})


