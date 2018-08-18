from django.db import models
from django.utils.timezone import now
from django.conf import settings
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from datetime import timedelta


class PresenceManager(models.Manager):
    def touch(self,channel_name):
        """
        presenceがRoomにいる時間を更新
        """
        self.filter(channel_name=channel_name).update(last_seen=now())

    def leave_all(self,channel_name):
        """
        すべての部屋からこのPresenceインスタンスを削除
        """
        # select_relatedを使うと外部キーのテーブルを取得しキャッシュできる
        for presence in self.select_related('room').filter(channel_name=channel_name):
            room = presence.room
            room.remove_presence(presence=presence)
    
class Presence(models.Model):
    room = models.ForeignKey('Room',on_delete=models.CASCADE)   # 外部キーroom
    channel_name = models.CharField(max_length=255)             # channel名
    # ユーザーはカスタマイズすることを考えてsettingsから取ってくる
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    # auto_nowやauto_now_addを使うと時間の自由な更新ができなくなるためdatetime.nowを使用
    last_seen = models.DateTimeField(default=now)
    objects = PresenceManager()
    def __sr__(self):
        return self.channel_name

    class Meta:
        # 部屋ごとに同じchannel_nameは一人まで
        unique_together = [('room','channel_name')]

class RoomManager(models.Manager):
    def add(self,room_channel_name,user_channel_name,user=None):
        """
        user_channel_nameをroom_channel_nameと名前のついたRoomに追加.
        もし必要ならRoom,Presenceインスタンスの作成,Groopの追加も行う.
        """
        # Roomの取得,なければ作成
        room,created = Room.objects.get_or_create(channel_name=room_channel_name)
        room.add_presence(user_channel_name)
        return room
    def remove(self,room_channel_name,user_channel_name):
        """
        user_channel_nameをroom_channel_nameで指定されたRoomから削除
        それに対するPresenceインスタンスも削除しGroupを更新
        """
        # 指定されたRoomが存在すれば取得
        try:
            room = Room.objects.get(channel_name=room_channel_name)
        except Room.DoesNotExist:
            return
        room.remove_presence(user_channel_name)
    def prune_presences(self,channel_layer=None,age=None):
        """
        age_in_secondsより前のlast_seenのPresenceインスタンスを削除する
        age_in_secondsはsettings.CHANNEL_PRESENCE_MAX_AGEでデフォルト値を定義できる
        """
        for room in Room.objects.all():
            room.prune_presences(age)
    def prune_rooms(self):
        """
        PresenceインスタンスのないRoomを削除
        """
        Room.objects.filter(presence__isnull=True).delete()

class Room(models.Model):
    channel_name = models.CharField(max_length=255,unique=True)
    objects = RoomManager()
    def __str_(self):
        return self.channel_name
    
    def add_presence(self,channel_name):
        """
        ユーザーが認証済か確認しPresenceインスタンスを作成
        """
        # 認証状態の確認
        # authenticated = user and(
        #     callable(user.is_authenticated) and user.is_authenticated()
        # )
        presence , created = Presence.objects.get_or_create(
            room = self,
            channel_name = channel_name
        )
        if created:
            channel_layer = get_channel_layer()
            # グループにチャンネルを追加
            channel_layer.add(self.channel_name,channel_name)
            self.broadcast_channged(added=presence)
    def remove_presence(self,channel_name=None,presence=None):
        """
        channel_nameをroomから削除
        presenceかchannel_nameを指定
        """
        if presence is None:
            try:
                presence = Presence.objects.get(room=self,channel_name=channel_name)
            except Presence.DoesNotExist:
                return
        # グループからchannel_nameを削除
        channel_layer = get_channel_layer()
        channel_layer.discard(self.channel_name,channel_name)
        # presenceインスタンスを削除
        presence.delete()
        self.broadcast_channged(removed=presence)
    def prune_presences(self,age_in_seconds=None):
        if age_in_seconds is None:
            # settings.pyからCHANNELS_PRESENCE_MAX_AGEを取得(default=60))
            age_in_seconds = getattr(settings , "CHANNELS_PRESENCE_MAX_AGE",60)
        # age_in_secondsより長い時間更新されていないPresenceを削除
        num_deleted,num_per_type = Presence.objects.filter(
            room=self,
            last_seend__lt=now() - timedelta(seconds=age_in_seconds)
        ).delete()
        if num_deleted > 0:
            self.broadcast_channged(bulk_change=True)
        
    def get_users(self):
        """
        Room内の認証済ユーザーリストを返す
        """
        # User = get_user_model()
        # return User.objects.filter(presence__room=self).distinct()
        pass
    def get_anonymous_count(self):
        """
        userがNoneのpresenseをすべて取得
        [CHANGED]
        """
        # return self.presence_set.filter(user=None).count()
        return self.presence_set.all()
    def broadcast_channged(self,added=None,removed=None,bulk_change=False):
        presence_changed.send(
            sender=self.__class__,
            room=self,
            added=added,
            removed=removed,
            bulk_change=bulk_change
        )




