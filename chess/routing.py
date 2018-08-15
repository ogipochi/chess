from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter ,URLRouter
import chess.routing

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            chess.routing.websocket_urlpatterns
        )
    )
})