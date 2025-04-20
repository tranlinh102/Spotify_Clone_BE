from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, AlbumViewSet, SongViewSet, FavoritesViewSet, DownloadViewSet, AlbumSongViewSet, FollowersViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'favorites', FavoritesViewSet)
router.register(r'downloads', DownloadViewSet)
router.register(r'album-songs', AlbumSongViewSet)
router.register(r'followers', FollowersViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]