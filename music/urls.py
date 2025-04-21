from django.urls import path

from music.views import SongUploadView
from .views import SongDeleteView, SongListView, LatestSongsView

urlpatterns = [
    path('add-song/', SongUploadView.as_view(), name='SongUploadView'),
    path('songs/', LatestSongsView.as_view(), name='song-8-list'),
    path('songs/<int:song_id>/', SongDeleteView.as_view(), name='song-delete'),
]