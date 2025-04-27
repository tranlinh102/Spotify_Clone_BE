from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PlaylistSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Album
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    artists = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = '__all__'

    def get_artists(self, obj):
        artist_songs = obj.artistsong_set.all()
        return ArtistSerializer([artist_song.artist for artist_song in artist_songs], many=True).data

class ArtistSongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    song = SongSerializer(read_only=True)

    class Meta:
        model = ArtistSong
        fields = '__all__'

class PlaylistSongSerializer(serializers.ModelSerializer):
    playlist = PlaylistSerializer(read_only=True)
    song = SongSerializer(read_only=True)

    class Meta:
        model = PlaylistSong
        fields = '__all__'

class AlbumSongSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    song = SongSerializer(read_only=True)

    class Meta:
        model = AlbumSong
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    song = SongSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'

class DownloadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    song = SongSerializer(read_only=True)

    class Meta:
        model = Download
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
