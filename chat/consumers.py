import json

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.api.serializers import serialize_author
from .models import Message, Chat, Contact
# from .views import get_last_10_messages, get_user_contact, get_current_chat
from .views import get_last_10_messages

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        # self.send_message(content)

    def new_message(self, data):
        # user_contact = get_user_contact(data['from'])
        current_user = self.scope['user']

        # current_chat = get_current_chat(data['chatId'])
        current_chat = Chat.objects.get(id=data['chatId'])
        contact_author = current_chat.participants.all().filter(user=current_user).get()
        # if not current_chat.participants.all().filter(user=user_contact).exists():
        #     raise Exception('403')

        message = Message.objects.create(
            author=contact_author,
            content=data['message'],
            chat=current_chat
        )

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            # 'author': message.author.user.username,
            'author': serialize_author(message.author.user),
            'content': message.content,
            # 'avatar': img.url,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        assert self.scope['user'].is_authenticated

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('WS connected %r listen room %r' % (self.scope['user'].username, self.room_name))

        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
