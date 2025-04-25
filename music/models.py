from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Artists(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    # class Meta:
    #     db_table = 'artists'
    #     managed = False

class Albums(models.Model):
    album_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    # class Meta:
    #     db_table = 'albums'
    #     managed = False

class Songs(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artists, models.DO_NOTHING, blank=True, null=True)
    duration = models.IntegerField()
    file_path = models.FileField(upload_to='songs/', max_length=255)
    video_url = models.FileField(upload_to='video/', max_length=255, blank=True, null=True)
    content_type = models.CharField(max_length=7)
    created_at = models.DateTimeField(blank=True, null=True)

    # class Meta:
    #     db_table = 'songs'
