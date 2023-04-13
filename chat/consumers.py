import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import Message, User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        author_id = text_data_json["a"]
        chat_id = text_data_json["chat"]

        message_create = Message(content=message, author_id=author_id, chat_id=chat_id)
        message_create.save()

        print("message:", message, "author_id:", author_id, "chat_id:", chat_id)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "author_id": author_id,
                "chat_id": chat_id
            }
        )

    def chat_message(self, event):
        message = event["message"]
        author_id = event["author_id"]
        author_username = User.objects.get(id=author_id).username
        chat_id = event["chat_id"]

        self.send(text_data=json.dumps({
            "type": "chat",
            "message": message,
            "chat_id": chat_id,
            "author_id": author_id,
            "author_username": author_username
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


class SideBarConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test"
        self.room_group_name = "all_users"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_id = text_data_json["chat"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "chat_id": chat_id
            }
        )

    def chat_message(self, event):
        message = event["message"]
        chat_id = event["chat_id"]

        self.send(text_data=json.dumps({
            "type": "chat",
            "message": message,
            "chat_id": chat_id,
        }))

    def chat_create(self, event):
        title = event["title"]
        users = event["users"]
        id = event["id"]
        type = "new-chat"
        self.send(text_data=json.dumps({"type": type, "users": users, "chat_id": id, "title": title}))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
