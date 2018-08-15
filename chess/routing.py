from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter ,URLRouter
import chess.routing

# RouterはsettingにASGI_APPLICATIONとしてパスを生成する
application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            battle.routing.websocket_urlpatterns
        )
    )
})