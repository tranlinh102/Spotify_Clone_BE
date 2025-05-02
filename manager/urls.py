from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,PlaylistViewSet, PlaylistSongViewSet, ArtistViewSet, AlbumViewSet, SongViewSet, FavoriteViewSet, DownloadViewSet, AlbumSongViewSet, FollowerViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'downloads', DownloadViewSet)
router.register(r'albumsongs', AlbumSongViewSet)
router.register(r'followers', FollowerViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'playlistsongs', PlaylistSongViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]