from channels.auth import AuthMiddlewareStack  # type: ignore
from channels.routing import URLRouter  # type: ignore
from channels.security.websocket import (
    AllowedHostsOriginValidator,  # type: ignore
)
from django.urls import path

from common import consumers

urlpatterns = [
    path(
        "ws/order/<str:uid>/",
        consumers.OrderConsumer.as_asgi(),
    ),
]

routes = AllowedHostsOriginValidator(
    AuthMiddlewareStack(consumers.QueryAuthMiddleware(URLRouter(urlpatterns)))
)
