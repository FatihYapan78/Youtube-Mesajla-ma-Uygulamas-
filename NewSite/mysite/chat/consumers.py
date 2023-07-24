# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *

class ChatConsumer(WebsocketConsumer):
    # Bağlantı başladığında çalışır
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
    # WEbsoket bağlantısı kapandığında çalışır.
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # WEbsoketten mesaj geldiğinde çalışır
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']
        tipi_nedir = text_data_json['tipi_nedir']
        m = Message.objects.create(content=message,user=user,room_id=self.room_name,tipi_nedir=tipi_nedir)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message", 
                "message": message,
                'user':user.username,
                'date': m.get_short_date(),
                'tipi_nedir':tipi_nedir,
                }
        )

    # Django tarafından istemciye mesajı yollar
    def chat_message(self, event):
        message = event["message"]
        user = event['user']
        date = event['date']
        tipi_nedir = event['tipi_nedir']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            'user':user,
            'date':date,
            'tipi_nedir':tipi_nedir,
            }))