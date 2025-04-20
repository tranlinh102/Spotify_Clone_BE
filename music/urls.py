from django.urls import path

from music.views import SongUploadView
from .views import SongListView

urlpatterns = [
    path('add-song/', SongUploadView.as_view(), name='SongUploadView'),
    path('songs/', SongListView.as_view(), name='song-list'),
]