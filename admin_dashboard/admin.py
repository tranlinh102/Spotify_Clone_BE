# from django.contrib import admin
# from manager.models import Artist, Album, Song, Favorite, Download, AlbumSong, Follower, Message
# @admin.register(Artist)
# class ArtistAdmin(admin.ModelAdmin):
#     list_display = ('artist_id', 'name', 'created_at')
#     search_fields = ('name',)
#     list_filter = ('created_at',)

# @admin.register(Album)
# class AlbumAdmin(admin.ModelAdmin):
#     list_display = ('album_id', 'title', 'created_by', 'created_at')
#     search_fields = ('title',)
#     list_filter = ('created_at',)

# @admin.register(Song)
# class SongAdmin(admin.ModelAdmin):
#     list_display = ('song_id', 'title', 'artist', 'duration', 'content_type', 'created_at')
#     search_fields = ('title', 'artist__name')
#     list_filter = ('content_type', 'created_at')
# # Register your models here.
