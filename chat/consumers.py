from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # 接続の受付
        print('[action]connect')
        
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # テキストデータを受け付け同じ内容をwebsocketに返す
        print('[action]receive')
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))