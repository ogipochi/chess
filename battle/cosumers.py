from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
# Consumerは以下の各種の機能を持つ
# event loopの処理を書かなくても,イベントが起きたときの処理だけ書いておけば良い
# 非同期,同期の処理

#Consumerのどの処理に送られるかは送られたデータのtypeキーの値による
# 例 : type:websocket.acceptの場合
#       def websocket_acceptに送られる

# self.sendメソッドはプロトコルで指定されたプロトコルサーバーかclientにeventを返す



# 同期処理の例
class EchoConsumer(SyncConsumer):
    """
    受け取ったtextキーのデータをそのまま返す
    """
    def websocket_connect(self,event):
        self.send({
            "type":"websocket.accept",
        })
    def websocket_receive(self,event):
        self.send({
            "type":"websocket.send",
            "text":event["text"]
        })

