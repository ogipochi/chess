from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/waiting/(?P<username>[^/]+)/$', consumers.WaitingConsumer),
    url(r'^ws/battle/$',consumers.BattleConsumer),
]