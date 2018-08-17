from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json


class WaitingConsumer(WebsocketConsumer):
    def connect(self):
        """
        ユーザー追加
        ユーザーリストを返す
        """
        print("[WaitingConsumer]Connect")
        self.accept()
    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """
        戦いたいユーザーを受け取る
        urlを返す(時間関数のハッシュ)).
        """
        print("[WaitingConsumer]Receive")
        # channel_layer = get_channel_layer()
        # ch_group_list = channel_layer.group_channels('<your group name>')
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