from django.shortcuts import render, get_object_or_404
import boto3
from decouple import config
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from manager.models import Album, Artist, Favorite, Follower, Song, Playlist, PlaylistSong
from manager.serializers import *

class SongUploadView(APIView):
    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Song uploaded successfully",
                "song": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongDeleteView(APIView):
    def delete(self, request, song_id):
        # Lấy bài hát từ cơ sở dữ liệu
        song = get_object_or_404(Song, song_id=song_id)
        
        # Xóa file trên S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        )
        try:
            s3.delete_object(Bucket=config('AWS_STORAGE_BUCKET_NAME'), Key=str(song.file_path))
        except Exception as e:
            return Response({"error": f"Failed to delete file from S3: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Xóa bài hát khỏi cơ sở dữ liệu
        song.delete()
        return Response({"message": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class LatestSongsView(ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.prefetch_related('artistsong_set__artist')[:8]

class LatestPlaylistsView(ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.select_related('created_by')[:4]

class PlaylistSongsView(ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')  # Lấy playlist_id từ URL
        return Song.objects.filter(playlistsong__playlist_id=playlist_id).prefetch_related('artistsong_set__artist')

class CreatePlaylistView(APIView):
    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                "message": "Playlist created successfully",
                "playlist": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPlaylistsView(ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(created_by=self.request.user).order_by('-created_at')
    
class AddSongToPlaylistView(APIView):
    def post(self, request):
        playlist_id = request.data.get('playlist_id')
        song_id = request.data.get('song_id')

        # Kiểm tra playlist và bài hát có tồn tại không
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id)
        song = get_object_or_404(Song, song_id=song_id)

        # Kiểm tra xem bài hát đã có trong playlist chưa
        if PlaylistSong.objects.filter(playlist=playlist, song=song).exists():
            return Response({"message": "Song already exists in the playlist"}, status=status.HTTP_400_BAD_REQUEST)

        # Thêm bài hát vào playlist
        PlaylistSong.objects.create(playlist=playlist, song=song)
        return Response({"message": "Song added to playlist successfully"}, status=status.HTTP_201_CREATED)

class UserFollowedArtistsView(ListAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        # Lấy danh sách nghệ sĩ mà người dùng hiện tại đang theo dõi
        return Artist.objects.filter(follower__user=self.request.user).distinct()

class FollowArtistView(APIView):
    def post(self, request):
        artist_id = request.data.get('artist_id')

        # Kiểm tra nghệ sĩ có tồn tại không
        artist = get_object_or_404(Artist, artist_id=artist_id)

        # Kiểm tra xem người dùng đã theo dõi nghệ sĩ này chưa
        if Follower.objects.filter(user=request.user, artist=artist).exists():
            return Response({"message": "You are already following this artist"}, status=status.HTTP_400_BAD_REQUEST)

        # Thêm dòng mới vào bảng Follower
        Follower.objects.create(user=request.user, artist=artist)
        return Response({"message": "Artist followed successfully"}, status=status.HTTP_201_CREATED)

class UnfollowArtistView(APIView):
    def delete(self, request):
        artist_id = request.data.get('artist_id')

        # Kiểm tra nghệ sĩ có tồn tại không
        artist = get_object_or_404(Artist, artist_id=artist_id)

        # Kiểm tra xem người dùng có đang theo dõi nghệ sĩ này không
        follower = Follower.objects.filter(user=request.user, artist=artist).first()
        if not follower:
            return Response({"message": "You are not following this artist"}, status=status.HTTP_400_BAD_REQUEST)

        # Xóa dòng trong bảng Follower
        follower.delete()
        return Response({"message": "Artist unfollowed successfully"}, status=status.HTTP_200_OK)

class RemoveSongFromPlaylistView(APIView):
    def delete(self, request):
        playlist_id = request.data.get('playlist_id')
        song_id = request.data.get('song_id')

        # Kiểm tra playlist và bài hát có tồn tại không
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id)
        song = get_object_or_404(Song, song_id=song_id)

        # Kiểm tra xem bài hát có trong playlist không
        playlist_song = PlaylistSong.objects.filter(playlist=playlist, song=song).first()
        if not playlist_song:
            return Response({"message": "Song not found in the playlist"}, status=status.HTTP_400_BAD_REQUEST)

        # Xóa bài hát khỏi playlist
        playlist_song.delete()
        return Response({"message": "Song removed from playlist successfully"}, status=status.HTTP_200_OK)
    
class UserFavoriteSongsView(ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        # Lấy danh sách bài hát yêu thích của người dùng hiện tại, sắp xếp theo thứ tự thêm vào (cũ nhất trước)
        return Song.objects.filter(favorite__user=self.request.user).order_by('favorite__added_at').distinct()
    
class AddSongToFavoritesView(APIView):
    def post(self, request):
        song_id = request.data.get('song_id')

        # Kiểm tra bài hát có tồn tại không
        song = get_object_or_404(Song, song_id=song_id)

        # Kiểm tra xem bài hát đã có trong danh sách yêu thích chưa
        if Favorite.objects.filter(user=request.user, song=song).exists():
            return Response({"message": "Song is already in favorites"}, status=status.HTTP_400_BAD_REQUEST)

        # Thêm bài hát vào danh sách yêu thích
        Favorite.objects.create(user=request.user, song=song)
        return Response({"message": "Song added to favorites successfully"}, status=status.HTTP_201_CREATED)

class RemoveSongFromFavoritesView(APIView):
    def delete(self, request):
        song_id = request.data.get('song_id')

        # Kiểm tra bài hát có tồn tại không
        song = get_object_or_404(Song, song_id=song_id)

        # Kiểm tra xem bài hát có trong danh sách yêu thích không
        favorite = Favorite.objects.filter(user=request.user, song=song).first()
        if not favorite:
            return Response({"message": "Song is not in favorites"}, status=status.HTTP_400_BAD_REQUEST)

        # Xóa bài hát khỏi danh sách yêu thích
        favorite.delete()
        return Response({"message": "Song removed from favorites successfully"}, status=status.HTTP_200_OK)

class PlaylistDetailView(APIView):
    def get(self, request, playlist_id):
        # Lấy thông tin playlist
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id)
        playlist_serializer = PlaylistSerializer(playlist)

        # Kiểm tra xem người dùng hiện tại có phải là người tạo playlist không
        is_owner = playlist.created_by == request.user

        # Lấy danh sách bài hát trong playlist (tận dụng PlaylistSongsView)
        songs = Song.objects.filter(playlistsong__playlist_id=playlist_id).prefetch_related('artistsong_set__artist')
        songs_serializer = SongSerializer(songs, many=True)

        return Response({
            "playlist": playlist_serializer.data,
            "is_owner": is_owner,
            "songs": songs_serializer.data
        }, status=status.HTTP_200_OK)
    
class ArtistSongsView(ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        artist_id = self.kwargs.get('artist_id')  # Lấy artist_id từ URL
        return Song.objects.filter(artistsong__artist_id=artist_id).prefetch_related('artistsong_set__artist')

class ArtistDetailView(APIView):
    def get(self, request, artist_id):
        # Lấy thông tin nghệ sĩ
        artist = get_object_or_404(Artist, artist_id=artist_id)
        artist_serializer = ArtistSerializer(artist)

        # Kiểm tra xem người dùng có theo dõi nghệ sĩ này không
        is_following = Follower.objects.filter(user=request.user, artist=artist).exists()

        # Lấy danh sách bài hát của nghệ sĩ
        songs = Song.objects.filter(artistsong__artist_id=artist_id).prefetch_related('artistsong_set__artist')
        songs_serializer = SongSerializer(songs, many=True)

        # Lấy danh sách album của nghệ sĩ
        albums = Album.objects.filter(artist=artist)
        albums_serializer = AlbumSerializer(albums, many=True)

        return Response({
            "artist": artist_serializer.data,
            "is_following": is_following,
            "songs": songs_serializer.data,
            "albums": albums_serializer.data
        }, status=status.HTTP_200_OK)
    
class CheckSongFavoriteView(APIView):
    def get(self, request, song_id):
        # Kiểm tra bài hát có tồn tại không
        song = get_object_or_404(Song, song_id=song_id)

        # Kiểm tra xem người dùng hiện tại có yêu thích bài hát này không
        is_favorite = Favorite.objects.filter(user=request.user, song=song).exists()

        return Response({
            "song_id": song_id,
            "is_favorite": is_favorite
        }, status=status.HTTP_200_OK)
    
class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')  # Lấy chuỗi tìm kiếm từ query parameter

        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Tìm kiếm gần giống trong Song, Playlist, Artist, và Album
        songs = Song.objects.filter(Q(title__icontains=query))
        playlists = Playlist.objects.filter(Q(title__icontains=query))
        artists = Artist.objects.filter(Q(name__icontains=query))
        albums = Album.objects.filter(Q(title__icontains=query))
        users = User.objects.filter(Q(username__icontains=query), is_staff = False, is_active=True, is_superuser=False).distinct()

        # Serialize dữ liệu
        songs_serializer = SongSerializer(songs, many=True)
        playlists_serializer = PlaylistSerializer(playlists, many=True)
        artists_serializer = ArtistSerializer(artists, many=True)
        albums_serializer = AlbumSerializer(albums, many=True)
        users_serializer = UserSerializer(users, many=True)

        return Response({
            "songs": songs_serializer.data,
            "playlists": playlists_serializer.data,
            "artists": artists_serializer.data,
            "albums": albums_serializer.data,
            "users": users_serializer.data
        }, status=status.HTTP_200_OK)
    
class OldestArtistsView(ListAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        # Lấy 8 nghệ sĩ cũ nhất dựa trên thời gian tạo (created_at)
        return Artist.objects.all()[:4]
    
class DeletePlaylistView(APIView):
    def delete(self, request, playlist_id):
        # Lấy playlist từ cơ sở dữ liệu
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id)

        # Kiểm tra xem người dùng hiện tại có phải là người tạo playlist không
        if playlist.created_by != request.user:
            return Response({"error": "You do not have permission to delete this playlist."}, status=status.HTTP_403_FORBIDDEN)

        # Xóa playlist
        playlist.delete()
        return Response({"message": "Playlist deleted successfully."}, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    def get(self, request, user_id):
        # Lấy thông tin người dùng từ cơ sở dữ liệu
        user = get_object_or_404(User, id=user_id)

        # Serialize dữ liệu người dùng
        user_serializer = UserSerializer(user)

        # Lấy danh sách playlist mà người dùng đã tạo
        playlists = Playlist.objects.filter(created_by=user)
        playlist_serializer = PlaylistSerializer(playlists, many=True)

        return Response({
            "user": user_serializer.data,
            "playlists": playlist_serializer.data
        }, status=status.HTTP_200_OK)

class AlbumDetailView(APIView):
    def get(self, request, album_id):
        # Lấy thông tin album từ cơ sở dữ liệu
        album = get_object_or_404(Album, album_id=album_id)
        album_serializer = AlbumSerializer(album)

        # Lấy danh sách bài hát trong album
        songs = getAlbumSongs(album_id)
        songs_serializer = SongSerializer(songs, many=True)

        return Response({
            "album": album_serializer.data,
            "songs": songs_serializer.data
        }, status=status.HTTP_200_OK)
    
class AlbumSongsView(APIView):
    def get(self, request, album_id):

        # Lấy danh sách bài hát
        songs = getAlbumSongs(album_id)

        # Serialize danh sách bài hát
        songs_serializer = SongSerializer(songs, many=True)

        # Trả về Response
        return Response(songs_serializer.data, status=status.HTTP_200_OK)
    
def getAlbumSongs(album_id):
    # Lấy thông tin album từ cơ sở dữ liệu
    album = get_object_or_404(Album, album_id=album_id)

    return Song.objects.filter(albumsong__album=album).prefetch_related('artistsong_set__artist')

class UpdatePlaylistView(APIView):
    def put(self, request, playlist_id):
        # Lấy playlist từ cơ sở dữ liệu
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id)

        # Kiểm tra xem người dùng hiện tại có phải là người tạo playlist không
        if playlist.created_by != request.user:
            return Response({"error": "You do not have permission to update this playlist."}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra và xóa ảnh cũ nếu có
        if 'image' in request.data and playlist.image:
            playlist.image.delete(save=False)  # Xóa ảnh cũ mà không lưu lại đối tượng

        # Cập nhật tên và hình ảnh của playlist
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Playlist updated successfully.",
                "playlist": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)