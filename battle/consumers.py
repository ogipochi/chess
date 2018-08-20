from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from presences.models import Room,Presence
from django.dispatch import receiver

from presences.signals import presence_changed
from django.core import serializers




class WaitingConsumer(AsyncWebsocketConsumer):
    groups = ['waiting']
    async def connect(self):
        """
        ユーザー追加
        ユーザーリストを返す
        """
        await self.accept()
        print("username",self.scope['url_route']['kwargs']['username'])
        self.username = self.scope['url_route']['kwargs']['username']
        # Groupに追加
        await self.channel_layer.group_add(
            'waiting',self.username)
        # Roomに追加    
        self.room = Room.objects.add("waiting", self.username)

        await self.channel_layer.group_send(
            'waiting',{
                'type':'user_list',
            }
        )
        channel_layer = get_channel_layer()
        print('チャンネル有効期限',channel_layer.group_expiry)
        
    async def user_list(self,event):
        await self.send(
        serializers.serialize(
                    "json",self.room.get_all_presence()
                    )
        )
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'waiting',self.username)
        Room.objects.remove("waiting",self.username)

    async def receive(self, text_data):
        """
        戦いたいユーザーを受け取る
        urlを返す(時間関数のハッシュ)).
        """
        print(text_data)
        text_json = json.loads(text_data)
        # if text_json["type"] == 'heartbeat':
        #     print("Renew")
        #     Presence.objects.touch(self.username)
        print("[WaitingConsumer]Receive")
        print(self.channel_layer)
        print(self.channel_name)
        await self.channel_layer.group_send(
            'waiting',{
                'type':'user_list',
            }
        )
    # @receiver(presence_changed)
    # async def broadcast_presence(self,room,**kwargs):
    #     self.channel_layer.group_send(
    #         'waiting',
    #         {
    #             'text':json.dumps({
    #                 'type':'presence',
    #                 'payload':{
    #                     'channel_name':self.channel_name,
    #                 }
    #             })
    #         }
    #     )
        
        
        
        # channel_layer = get_channel_layer()

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # channel_layer.send("channel_name", {
        #     "type": "chat.message",
        #     "text": "Hello there!",
        #     })

class BattleConsumer(WebsocketConsumer):
    def connect(self):
        """
        接続のみ
        
        """

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """

        バトルデータの通信
        """
        print('[action]receive')
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))