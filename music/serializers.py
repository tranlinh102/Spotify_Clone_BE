from rest_framework import serializers
from .models import Artist, Album, Song, AlbumSong, Favorite, Download, Follower, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['artist_id', 'name', 'bio', 'created_at']

class AlbumSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Album
        fields = ['album_id', 'title', 'created_by', 'created_at']

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    class Meta:
        model = Song
        fields = ['song_id', 'title', 'artist', 'duration', 'file_path', 'video_url', 'content_type', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ['user', 'song', 'added_at']

class DownloadSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Download
        fields = ['user', 'song', 'downloaded_at']

class AlbumSongSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    class Meta:
        model = AlbumSong
        fields = ['album', 'song']

class FollowersSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Follower
        fields = ['user', 'artist', 'followed_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'sent_at']