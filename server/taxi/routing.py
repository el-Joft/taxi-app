import os
from django.core.asgi import get_asgi_application
from django.urls import path # new
from channels.routing import ProtocolTypeRouter, URLRouter # changed

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi.settings")

from .middleware import TokenAuthMiddlewareStack
from trips.consumers import TaxiConsumer


application = ProtocolTypeRouter({
   # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # WebSocket chat handler
    "websocket": TokenAuthMiddlewareStack(URLRouter([
        path('taxi/', TaxiConsumer.as_asgi()),
    ]),
    ),
})
