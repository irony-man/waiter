from django.urls import path

from common import consumers

websocket_urlpatterns = [
    path("ws/order/<str:uid>/", consumers.OrderConsumer.as_asgi()),
]
