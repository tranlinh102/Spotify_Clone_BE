from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContentTypeStatsView, UserViewSet, PlaylistViewSet, PlaylistSongViewSet, ArtistSongViewSet, ArtistViewSet, AlbumViewSet, SongViewSet, FavoriteViewSet, DownloadViewSet, AlbumSongViewSet, FollowerViewSet, MessageViewSet


router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'downloads', DownloadViewSet)
router.register(r'album_songs', AlbumSongViewSet)
router.register(r'followers', FollowerViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'artist_songs', ArtistSongViewSet)
router.register(r'playlist_songs', PlaylistSongViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
     path('stats/content-type/', ContentTypeStatsView.as_view(), name='content_type_stats'),
]