# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):
    # Bağlantı başladığında çalışır
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()
    # WEbsoket bağlantısı kapandığında çalışır.
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # WEbsoketten mesaj geldiğinde çalışır
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']
        tipi_nedir = text_data_json['tipi_nedir']
        await self.save_database(message,user,self.room_name,tipi_nedir)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message", 
                "message": message,
                'user':user.username,
                'date': self.message_object.get_short_date(),
                'tipi_nedir':tipi_nedir,
                }
        )

    # Django tarafından istemciye mesajı yollar
    async def chat_message(self, event):
        message = event["message"]
        user = event['user']
        date = event['date']
        tipi_nedir = event['tipi_nedir']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            'user':user,
            'date':date,
            'tipi_nedir':tipi_nedir,
            }))
    @database_sync_to_async
    def save_database(self,message,user,room,tipi_nedir):
        m = Message.objects.create(content=message,user=user,room_id=room,tipi_nedir=tipi_nedir)
        self.message_object = m