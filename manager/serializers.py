from rest_framework import serializers
from django.contrib.auth.models import User
from manager.models import *
from asgiref.sync import sync_to_async

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'email',
            'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class PlaylistSerializer(serializers.ModelSerializer):
    created_by_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='created_by'  # Ánh xạ với trường 'create_by' trong model playlist
    )
    class Meta:
        model = Playlist
        fields = ['playlist_id', 'title', 'image', 'created_at', 'created_by_id']
        read_only_fields = ['playlist_id', 'created_at', 'created_by_id']

class ArtistSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist'  # Ánh xạ với trường 'artist' trong model
    )

    class Meta:
        model = Album
        fields = ['album_id', 'title', 'image', 'artist_id', 'created_at']

class SongSerializer(serializers.ModelSerializer):
    artists = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = '__all__'

    def get_artists(self, obj):
        artist_songs = obj.artistsong_set.all()
        return ArtistSerializer([artist_song.artist for artist_song in artist_songs], many=True).data

class ArtistSongSerializer(serializers.ModelSerializer):
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist'  # Ánh xạ với trường 'artist' trong model
    )
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source='song'  # Ánh xạ với trường 'song' trong model
    )

    class Meta:
        model = ArtistSong
        fields = ['id','artist_id', 'song_id', 'main_artist', 'added_at']

class PlaylistSongSerializer(serializers.ModelSerializer):
    playlist_id = serializers.PrimaryKeyRelatedField(
        queryset=Playlist.objects.all(),
        source='playlist'  # Ánh xạ với trường 'playlist' trong model
    )
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source='song'  # Ánh xạ với trường 'song' trong model
    )

    class Meta:
        model = PlaylistSong
        fields = ['id', 'playlist_id', 'song_id', 'added_at']

class AlbumSongSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        source='album'  # Ánh xạ với trường 'album' trong model
    )
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source='song'  # Ánh xạ với trường 'song' trong model
    )

    class Meta:
        model = AlbumSong
        fields = ['id', 'album_id', 'song_id', 'added_at']

class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user'  # Ánh xạ với trường 'user' trong model
    )
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source='song'  # Ánh xạ với trường 'song' trong model
    )

    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'song_id', 'added_at']

class DownloadSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user'  # Ánh xạ với trường 'user' trong model
    )
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source='song'  # Ánh xạ với trường 'song' trong model
    )

    class Meta:
        model = Download
        fields = ['id', 'user_id', 'song_id', 'downloaded_at']

class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user'  # Ánh xạ với trường 'user' trong model
    )
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist'  # Ánh xạ với trường 'artist' trong model
    )

    class Meta:
        model = Follower
        fields = ['id', 'user_id', 'artist_id', 'followed_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender'  # Ánh xạ với trường 'sender' trong model
    )
    chatroom_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatRoom.objects.all(),
        source='chatroom'  # Ánh xạ với trường 'chatroom' trong model
    )

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender_id', 'chatroom_id', 'content', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    user1_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user1'  # Ánh xạ với trường 'user1' trong model
    )
    user2_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user2'  # Ánh xạ với trường 'user2' trong model
    )

    class Meta:
        model = ChatRoom
        fields = ['id', 'user1_id', 'user2_id', 'created_at']
    
class ChatRoomWithLastMessageSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    other_user_id = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'other_user_id', 'last_message']

    def get_last_message(self, obj):
        # Lấy tin nhắn mới nhất trong ChatRoom
        last_message = obj.chatmessage_set.order_by('-timestamp').first()
        if last_message:
            return {
                'id': last_message.id,
                'content': last_message.content,
                'sender_id': last_message.sender.id,
                'is_read': last_message.is_read,  # Trạng thái đã đọc
                'timestamp': last_message.timestamp
            }
        return None

    def get_other_user_id(self, obj):
        # Lấy ID của người còn lại trong ChatRoom
        request_user = self.context['request'].user
        if obj.user1 == request_user:
            return obj.user2.id
        return obj.user1.id
    
@sync_to_async
def save_serializer(serializer_class, data):
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()