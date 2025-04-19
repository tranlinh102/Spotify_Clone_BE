from django.urls import path

from music.views import SongUploadView

urlpatterns = [
    path('add-song/', SongUploadView.as_view(), name='SongUploadView'),
]