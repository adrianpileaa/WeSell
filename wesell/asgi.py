import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from channels.routing import get_default_application
import products.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesell.settings')
django_asgi_app = get_default_application()
django.setup()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            products.routing.websocket_urlpatterns
        )
    ),
})


