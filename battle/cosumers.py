from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer

# Consumerは以下の各種の機能を持つ
# event loopの処理を書かなくても,イベントが起きたときの処理だけ書いておけば良い
# 非同期,同期の処理
# 初期化された際にはconnectionのscopeを受け取る.このscopeはself.scopeで確認可能
# self.scope["path"]      : リクエストのpath
# self.scope["headers"]   : リクエストヘッダのキー/バリュー
# self.scope["method"]    : リクエストメソッド
# self.scope["user"]      : ユーザオブジェクト(Auth実装時のみ)
# self.scope["url_route"] : urlRouter(URLRouter)
# Djangoでよく使われるrequestと同じようにmiddlewareから情報が追加される.

#Consumerのどの処理に送られるかは送られたデータのtypeキーの値による
# 例 : type:websocket.acceptの場合
#       def websocket_acceptに送られる

# self.sendメソッドはプロトコルで指定されたプロトコルサーバーかclientにeventを返す



# 非同期通信の例
# class EchoConsumer(SyncConsumer):
#     """
#     受け取ったtextキーのデータをそのまま返す
#     """
#     def websocket_connect(self,event):
#         self.send({
#             "type":"websocket.accept",
#         })
#     def websocket_receive(self,event):
#         self.send({
#             "type":"websocket.send",
#             "text":event["text"]
#     })


# 同期通信の例
# class EchoConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         await self.send({
#             "type" : "websocket.accept",
#         })
#     async def websocket_receive(self,event):
#         await self.send({
#             "type":"websocket.send",
#             "text":event["text"]
#         })


from channels.generic.websocket import WebsocketConsumer


# WebSocketConsumerを使った例
# 自分で独自の認証メソッドなどを作成したい場合(mixinを使わない場合)
# 結果ごとにchannels.exceptions.AcceptConnection や channels.exceptions.DenyConnection
# をraiseすればいい
# groupsの名前が出ると自動的にその名前のgroupに追加される.


# class MyConsumer(WebsocketConsumer):
#     groups = ["broadcast"]
#     def connect(self):
#         """
#         connectionで呼ばれる
#         """

#         # connection callを受け取る場合
#         self.accept()
#         # self.scope['subprotocols']で定義されたサブプロトコルか判断して受け取る場合
#         self.accept('subprotocol')
#         # 拒否する場合
#         self.close()
#     def receive(self,text_data = None,bytes_data=None):
#         """
#         各フレームでtext_dataかbytesデータと一緒に呼ばれる
#         """
#         # テキストデータを送る場合
#         self.send(text_data='Hello World')
#         # バイトデータを送る場合
#         self.send(bytes_data='Hello World')

#         #強制クローズする場合
#         self.close()
#         #エラーコード込でクローズする場合
#         self.close(code=4123)

#     def disconnect(self,close_code):
#         # closeした時呼ばれる
#         pass



from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        """
        connectionで呼ばれる
        """
        # connection callをacceptする場合
        await self.accept()
        # 指定したsubprotocolを受け取る場合
        # 利用可能なsubprotocolのリストはself.scope["subprotocols"]で取得可能
        await self.accept("subprotocol")
        # connection callを拒否する場合
        await self.close()
    async def receive(self,text_data=None,bytes_data=None):
        """
        各フレームでtext dataかbytes dataを受け取る
        """
        # テキストデータを送る場合
        await self.send(text_data="Hello World")
        # バイナリデータを送る場合
        await self.send(bytes_data="Hello World")
        # connectionを閉じる場合
        await self.close()
        # カスタムのエラーコード
        await self.close(code=4123)

    async def disconnect(self,close_code):
        """
        closeした時呼ばれる
        """
        pass



