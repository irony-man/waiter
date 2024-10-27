import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer  # type: ignore
from loguru import logger

from common.serializers import OrderSerializer


class OrderConsumer(WebsocketConsumer):
    def get_room_name(self) -> str | None:
        user = self.scope["user"]
        if uid := self.scope["url_route"]["kwargs"].get("uid", None):
            if user.is_authenticated and str(uid) == str(user.userprofile.uid):
                return str(user.userprofile.chain.uid)
            return uid
        return None

    def connect(self):
        chat_room = self.get_room_name()
        self.chat_room = chat_room
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
        self.send(text_data=json.dumps(data))

    def send_order(self, event):
        self.send(
            text_data=json.dumps(OrderSerializer(instance=event["order"]).data)
        )
