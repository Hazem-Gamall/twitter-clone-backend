from channels.generic.websocket import WebsocketConsumer
import json
from .models import Chat, Message
from asgiref.sync import async_to_sync
from django.db.models import Q


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("hello")
        self.accept()
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        request_user = self.scope["user"]
        print("ws req user", request_user)
        target_chat = Chat.objects.filter(id=self.chat_id)
        if not target_chat.exists():
            self.close(code=4000)

        if not target_chat.filter(
            Q(first_user_profile=request_user.profile)
            | Q(second_user_profile=request_user.profile)
        ):
            self.close(code=4001)

        async_to_sync(self.channel_layer.group_add)(self.chat_id, self.channel_name)

    def disconnect(self, code):
        print("disconnecting")
        async_to_sync(self.channel_layer.group_discard)(self.chat_id, self.channel_name)

    # From WebSocket
    def receive(self, text_data=None):
        print(
            "text data",
            text_data,
        )
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        Message.objects.create(
            text=text_data, author=self.scope["user"], chat=self.chat_id
        )
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id, {"type": "receive_message", "message": message}
        )

    # From group/chat
    def receive_message(self, event):
        message = event["message"]

        print("sending back message to user")
        # Send back to the socket
        self.send(text_data=json.dumps({"message": message}))
