from rest_framework import serializers
from django.contrib.auth.models import User
from manager.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PlaylistSerializer(serializers.ModelSerializer):
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='create_by'  # Ánh xạ với trường 'create_by' trong model playlist
    )

    class Meta:
        model = Playlist
        fields = ['playlist_id', 'title', 'image', 'created_by_id', 'created_at']

class ArtistSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Song
        fields = '__all__'

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

class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender'  # Ánh xạ với trường 'sender' trong model
    )
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='receiver'  # Ánh xạ với trường 'receiver' trong model
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'receiver_id', 'message_text', 'sent_at']
