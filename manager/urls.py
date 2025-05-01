from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, AlbumViewSet, SongViewSet, FavoriteViewSet, DownloadViewSet, AlbumSongViewSet, FollowerViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'downloads', DownloadViewSet)
router.register(r'albumsongs', AlbumSongViewSet)
router.register(r'followers', FollowerViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]