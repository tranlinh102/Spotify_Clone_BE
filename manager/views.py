from django.shortcuts import render
from rest_framework import viewsets
from .models import Artist, Album, Song, Favorite, Download, AlbumSong, Follower, Message
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer, FavoriteSerializer, DownloadSerializer, AlbumSongSerializer, FollowersSerializer, MessageSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class DownloadViewSet(viewsets.ModelViewSet):
    queryset = Download.objects.all()
    serializer_class = DownloadSerializer

class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = AlbumSong.objects.all()
    serializer_class = AlbumSongSerializer

class FollowersViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowersSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# Create your views here.
