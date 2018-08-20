from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from presences.models import Room,Presence




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
        Room.objects.add("waiting", self.username)

        await self.channel_layer.group_send(
            'waiting',{
                'type':'user_list',
            }
        )
        await self.channel_layer.group_send(
            'waiting',
            {
                'type': 'chat_message',
                'message': 'hello world'
            }
        )
        channel_layer = get_channel_layer()
        print(dir(channel_layer))
        print(self.scope["user"])
        print(type(self.scope["user"]))
        print(dir(self.scope["user"]))
        print(self.scope["user"].is_authenticated())
        # print('channel_names',channel_layer.valid_channel_names())
        print('チャンネル有効期限',channel_layer.group_expiry)
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    async def user_list(self,event):
        print('hello world')
        await self.send(text_data=json.dumps({
            'message': 'hello'
        }))
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'waiting',self.username)
        Room.objects.remove("waiting",self.username)

    async def receive(self, text_data):
        """
        戦いたいユーザーを受け取る
        urlを返す(時間関数のハッシュ)).
        """
        if json.dumps(text_data)["message"] == '"heartbeat"':
            Presence.objects.touch(message.reply_channel.name)
        print("[WaitingConsumer]Receive")
        print(self.channel_layer)
        print(self.channel_name)
        await self.channel_layer.group_send(
            'waiting',{
                'type':'user_list',
            }
        )
        
        
        
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