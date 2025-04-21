from django.db import models
from django.contrib.auth.models import User


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True, null=True)  # URL to the playlist cover image
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'playlists'

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)  # URL to the profile picture
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'artists'

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True, null=True)  # URL to the album cover image
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'albums'

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True, null=True)  # URL to the song cover image
    file_path = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'audio/mpeg', 'video/mp4'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'songs'

class ArtistSong(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    main_artist = models.BooleanField(default=False)  # True if the artist is the main artist for the song
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artist', 'song')
        db_table = 'artist_songs'

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'song')
        db_table = 'playlist_songs'

class AlbumSong(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('album', 'song')
        db_table = 'album_songs'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        db_table = 'favorites'

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        db_table = 'downloads'

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artist')
        db_table = 'followers'

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    class Meta:
        db_table = 'messages'
# Create your models here.
