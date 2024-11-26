import json
from functools import partial

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async  # type: ignore
from channels.generic.websocket import WebsocketConsumer  # type: ignore
from django.shortcuts import get_object_or_404
from loguru import logger

from common.models import Order, Restaurant
from common.serializers import OrderSerializer


@database_sync_to_async
def get_queryset(scope) -> str | None:
    user = scope["user"]
    if user.is_authenticated:
        return Restaurant.objects.filter(chain=user.userprofile.chain)
    return Restaurant.objects.none()


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["queryset"] = await get_queryset(scope)
        return await self.app(scope, receive, send)


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        chat_room = self.scope["session"].get("uid", None)
        if uid := self.scope["url_route"]["kwargs"].get("uid", None):
            if self.scope["queryset"].filter(uid=uid).first():
                chat_room = str(uid)
        self.scope["chat_room"] = chat_room
        self.chat_room = self.scope["chat_room"]
        logger.info(f"Connected to {chat_room}")
        self.stop = False

        async_to_sync(self.channel_layer.group_add)(
            self.chat_room, self.channel_name
        )

        self.accept()

    def websocket_disconnect(self, message):
        return super().websocket_disconnect(message)

    def receive(self, text_data):
        data = json.loads(text_data)
        instance = get_object_or_404(Order, uid=data.get("uid"))
        instance.status = data.get("status", instance.status)
        instance.clean()
        instance.save()

    def send_order(self, event):
        self.send(
            text_data=json.dumps(OrderSerializer(instance=event["order"]).data)
        )
