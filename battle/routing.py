from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/waiting/$', consumers.WaitingConsumer),
    url(r'^ws/battle/$',consumers.BattleConsumer),
]