from django.urls import path

from music.views import SongUploadView
from .views import SongDeleteView, SongListView, LatestSongsView, LatestPlaylistsView, PlaylistSongsView

urlpatterns = [
    path('add-song/', SongUploadView.as_view(), name='SongUploadView'),
    path('songs/', LatestSongsView.as_view(), name='song-8-list'),
    path('songs/<int:song_id>/', SongDeleteView.as_view(), name='song-delete'),
    path('playlistsSuggested/', LatestPlaylistsView.as_view(), name='latest-playlists'),
    path('playlists/<int:playlist_id>/songs/', PlaylistSongsView.as_view(), name='playlist-songs'),
]