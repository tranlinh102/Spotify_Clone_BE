from django.urls import path

from music.views import SongUploadView
from .views import *

urlpatterns = [
    path('add-song/', SongUploadView.as_view(), name='SongUploadView'),
    path('songs/', LatestSongsView.as_view(), name='song-8-list'),
    path('songs/<int:song_id>/', SongDeleteView.as_view(), name='song-delete'),
    path('songs/favorites/', UserFavoriteSongsView.as_view(), name='user-favorite-songs'),
    path('songs/favorites/add/', AddSongToFavoritesView.as_view(), name='add-song-to-favorites'),
    path('songs/favorites/remove/', RemoveSongFromFavoritesView.as_view(), name='remove-song-from-favorites'),
    path('songs/<int:song_id>/is-favorite/', CheckSongFavoriteView.as_view(), name='check-song-favorite'),
    path('playlistsSuggested/', LatestPlaylistsView.as_view(), name='latest-playlists'),
    path('playlists/<int:playlist_id>/songs/', PlaylistSongsView.as_view(), name='playlist-songs'),
    path('playlists/create/', CreatePlaylistView.as_view(), name='create-playlist'),
    path('playlists/user/', UserPlaylistsView.as_view(), name='user-playlists'),
    path('playlists/add-song/', AddSongToPlaylistView.as_view(), name='add-song-to-playlist'),
    path('playlists/<int:playlist_id>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/remove-song/', RemoveSongFromPlaylistView.as_view(), name='remove-song-from-playlist'),
    path('playlists/<int:playlist_id>/delete/', DeletePlaylistView.as_view(), name='delete-playlist'),
    path('playlists/<int:playlist_id>/update/', UpdatePlaylistView.as_view(), name='update-playlist'),
    path('artists/followed/', UserFollowedArtistsView.as_view(), name='user-followed-artists'),
    path('artists/follow/', FollowArtistView.as_view(), name='follow-artist'),
    path('artists/unfollow/', UnfollowArtistView.as_view(), name='unfollow-artist'),
    path('artists/<int:artist_id>/songs/', ArtistSongsView.as_view(), name='artist-songs'),
    path('artists/<int:artist_id>/', ArtistDetailView.as_view(), name='artist-detail'),
    path('artists/suggested/', OldestArtistsView.as_view(), name='oldest-artists'),
    path('search/', SearchView.as_view(), name='search'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('albums/<int:album_id>/', AlbumDetailView.as_view(), name='album-detail'),
    path('albums/<int:album_id>/songs/', AlbumSongsView.as_view(), name='album-songs'),
]