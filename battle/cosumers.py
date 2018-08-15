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
class EchoConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        await self.send({
            "type" : "websocket.accept",
        })
    async def websocket_receive(self,event):
        await self.send({
            "type":"websocket.send",
            "text":event["text"]
        })
    


