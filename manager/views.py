from rest_framework import viewsets
from manager.models import (
    Playlist, Artist, ArtistSong, Album, Song, 
    Favorite, Download, AlbumSong, Follower, Message, PlaylistSong)
from .serializers import (
    PlaylistSerializer,ArtistSerializer, AlbumSongSerializer, 
    AlbumSerializer, SongSerializer, FavoriteSerializer, 
    DownloadSerializer, AlbumSongSerializer, FollowerSerializer, 
    MessageSerializer, ArtistSongSerializer, PlaylistSongSerializer)
import boto3
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from decouple import config
from rest_framework.decorators import action
from botocore.exceptions import PartialCredentialsError
from rest_framework.permissions import AllowAny
from django.db.models import Count


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

    @action(detail=False, methods=['post'], url_path='add')
    def add_playlist(self, request):
        try:
            data = request.data.copy()
            image_file = request.FILES.get('image')

            if image_file:
                data['image'] = image_file

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Playlist created successfully",
                "playlist": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create playlist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_playlist(self, request, pk=None):
        try:
            playlist = self.get_object()

            if playlist.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    file_path = playlist.image.name
                    s3 = self.get_s3_client()
                    s3.delete_object(Bucket=bucket_name, Key=file_path)
                except ClientError as e:
                    return Response({"warning": f"Playlist deleted but image not removed from S3: {str(e)}"}, status=status.HTTP_200_OK)

            playlist.delete()
            return Response({"message": "Playlist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete playlist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_playlist(self, request, pk=None):
        try:
            playlist = self.get_object()
            image_file = request.FILES.get('image')

            if image_file and playlist.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    old_file_path = playlist.image.name
                    s3 = self.get_s3_client()
                    s3.delete_object(Bucket=bucket_name, Key=old_file_path)
                except ClientError as e:
                    return Response({"warning": f"Old image not removed from S3: {str(e)}"}, status=status.HTTP_200_OK)

            serializer = self.get_serializer(playlist, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(image=image_file)

            return Response({
                "message": "Playlist updated successfully",
                "playlist": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update playlist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

    @action(detail=False, methods=['get'], url_path='count')
    def count_artists(self, request):
        try:
            total_artists = Artist.objects.count()  # Đếm tổng số nghệ sĩ
            return Response({
                "message": "Total artists count retrieved successfully",
                "total_artists": total_artists
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve artists count: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='add')
    def add_artist(self, request, *args, **kwargs):
        try:
            data = request.data
            image_file = request.FILES.get('image')

            # Nếu có file hình ảnh thì tự động lưu trữ trên S3 nhờ cấu hình đã có trong STORAGES
            if image_file:
                data['image'] = image_file  # Gán file vào trường 'image' để Django tự xử lý lưu lên S3
            else:
                data['image'] = None  # Nếu không có file, gán image là None

            # Tạo serializer và lưu dữ liệu
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Artist created successfully",
                "artist": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to create artist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_artist(self, request, pk=None):
        try:
            artist = self.get_object()

            if artist.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    file_path = artist.image.name  # Đường dẫn nội bộ trong S3

                    s3 = self.get_s3_client()
                    s3.delete_object(Bucket=bucket_name, Key=file_path)
                except ClientError as e:
                    return Response({"warning": f"Artist deleted but image not removed from S3: {str(e)}"}, status=status.HTTP_200_OK)

            artist.delete()
            return Response({"message": "Artist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete artist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_artist(self, request, pk=None):
        try:
            artist = self.get_object()
            image_file = request.FILES.get('image')

            # Nếu có ảnh mới, xóa ảnh cũ (Django-storages sẽ tự làm nếu gán field mới)
            if image_file and artist.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    old_file_path = artist.image.name
                    s3 = self.get_s3_client()
                    s3.delete_object(Bucket=bucket_name, Key=old_file_path)
                except ClientError as e:
                    return Response({"warning": f"Old image not removed from S3: {str(e)}"}, status=status.HTTP_200_OK)

            # Gửi dữ liệu cho serializer (gồm cả file nếu có)
            serializer = self.get_serializer(artist, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Artist updated successfully",
                "artist": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to update artist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes  = [AllowAny]

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

    @action(detail=False, methods=['post'], url_path='add')
    def add_album(self, request):
        try:
            data = request.data.copy()
            image_file = request.FILES.get('image')
            if image_file:
                data['image'] = image_file  # Django sẽ tự upload nếu S3 đã config đúng

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Album created successfully",
                "album": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": f"Failed to create album: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_album(self, request, pk=None):
        try:
            album = self.get_object()
            if album.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    file_path = album.image.name
                    s3 = self.get_s3_client()
                    s3.delete_object(Bucket=bucket_name, Key=file_path)
                except ClientError as e:
                    return Response({"warning": f"Album deleted but image not removed from S3: {str(e)}"}, status=status.HTTP_200_OK)
            
            album.delete() 
            return Response({"message": "Album deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete album: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_album(self, request, pk=None):
        try:
            album = self.get_object()
            image_file = request.FILES.get('image')

            # Nếu có ảnh mới, xóa ảnh cũ
            if image_file and album.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    old_file_path = album.image.name
                    s3 = self.get_s3_client()
                    s3.delete_object(Bucket=bucket_name, Key=old_file_path)
                except ClientError as e:
                    return Response({"warning": f"Old image not removed from S3: {str(e)}"}, status=status.HTTP_200_OK)

            # Gửi dữ liệu cho serializer
            serializer = self.get_serializer(album, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(image=image_file)  # Lưu file mới

            return Response({
                "message": "Album updated successfully",
                "album": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to update album: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny]

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

    @action(detail=False, methods=['post'], url_path='add')
    def add_song(self, request, *args, **kwargs):
        try:
            data = request.data
            # Nếu có file image, file_path hoặc video_url, gán vào để Django tự xử lý upload
            if 'image' in request.FILES:
                data['image'] = request.FILES['image']
            if 'file_path' in request.FILES:
                data['file_path'] = request.FILES['file_path']
            if 'video_url' in request.FILES:
                data['video_url'] = request.FILES['video_url']

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Song created successfully",
                "song": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to create song: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['put'], url_path='update')
    def update_song(self, request, pk=None):
        try:
            song = self.get_object()
            data = request.data
            s3 = self.get_s3_client()

            # Nếu có file mới thì xóa file cũ trên S3
            if 'image' in request.FILES and song.image:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    s3.delete_object(Bucket=bucket_name, Key=song.image.name)
                except ClientError as e:
                    return Response({"warning": f"Old image not removed: {str(e)}"}, status=status.HTTP_200_OK)

            if 'file_path' in request.FILES and song.file_path:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    s3.delete_object(Bucket=bucket_name, Key=song.file_path.name)
                except ClientError as e:
                    return Response({"warning": f"Old audio file not removed: {str(e)}"}, status=status.HTTP_200_OK)

            if 'video_url' in request.FILES and song.video_url:
                try:
                    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                    s3.delete_object(Bucket=bucket_name, Key=song.video_url.name)
                except ClientError as e:
                    return Response({"warning": f"Old video file not removed: {str(e)}"}, status=status.HTTP_200_OK)

            # Cập nhật file mới
            if 'image' in request.FILES:
                data['image'] = request.FILES['image']
            if 'file_path' in request.FILES:
                data['file_path'] = request.FILES['file_path']
            if 'video_url' in request.FILES:
                data['video_url'] = request.FILES['video_url']

            serializer = self.get_serializer(song, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Song updated successfully",
                "song": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to update song: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_song(self, request, pk=None):
        try:
            song = self.get_object()

            # Tự động xóa file trên S3 vì bạn đã override delete() trong model
            song.delete()

            return Response({"message": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": f"Failed to delete song: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArtistSongViewSet(viewsets.ModelViewSet):
    queryset = ArtistSong.objects.all()
    serializer_class = ArtistSongSerializer

    @action(detail=False, methods=['post'], url_path='add')
    def add_artist_song(self, request):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "ArtistSong created successfully",
                "artist_song": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create ArtistSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_artist_song(self, request, pk=None):
        try:
            artist_song = self.get_object()
            artist_song.delete()

            return Response({"message": "ArtistSong deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete ArtistSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_artist_song(self, request, pk=None):
        try:
            artist_song = self.get_object()
            serializer = self.get_serializer(artist_song, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "ArtistSong updated successfully",
                "artist_song": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update ArtistSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlaylistSongViewSet(viewsets.ModelViewSet):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer

    @action(detail=False, methods=['post'], url_path='add')
    def add_playlist_song(self, request):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "PlaylistSong created successfully",
                "playlist_song": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create PlaylistSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_playlist_song(self, request, pk=None):
        try:
            playlist_song = self.get_object()
            playlist_song.delete()

            return Response({"message": "PlaylistSong deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete PlaylistSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_playlist_song(self, request, pk=None):
        try:
            playlist_song = self.get_object()
            serializer = self.get_serializer(playlist_song, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "PlaylistSong updated successfully",
                "playlist_song": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update PlaylistSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = AlbumSong.objects.all()
    serializer_class = AlbumSongSerializer

    @action(detail=False, methods=['post'], url_path='add')
    def add_album_song(self, request):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "AlbumSong created successfully",
                "album_song": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create AlbumSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_album_song(self, request, pk=None):
        try:
            album_song = self.get_object()
            album_song.delete()

            return Response({"message": "AlbumSong deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete AlbumSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_album_song(self, request, pk=None):
        try:
            album_song = self.get_object()
            serializer = self.get_serializer(album_song, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "AlbumSong updated successfully",
                "album_song": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update AlbumSong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    @action(detail=False, methods=['post'], url_path='add')
    def add_favorite(self, request):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Favorite created successfully",
                "favorite": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create Favorite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_favorite(self, request, pk=None):
        try:
            favorite = self.get_object()
            favorite.delete()

            return Response({"message": "Favorite deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete Favorite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_favorite(self, request, pk=None):
        try:
            favorite = self.get_object()
            serializer = self.get_serializer(favorite, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Favorite updated successfully",
                "favorite": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update Favorite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadViewSet(viewsets.ModelViewSet):
    queryset = Download.objects.all()
    serializer_class = DownloadSerializer

    @action(detail=False, methods=['post'], url_path='add')
    def add_download(self, request):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Download created successfully",
                "download": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create Download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_download(self, request, pk=None):
        try:
            download = self.get_object()
            download.delete()

            return Response({"message": "Download deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete Download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_download(self, request, pk=None):
        try:
            download = self.get_object()
            serializer = self.get_serializer(download, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Download updated successfully",
                "download": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update Download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    @action(detail=False, methods=['post'], url_path='add')
    def add_follower(self, request):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Follower added successfully",
                "follower": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to add Follower: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_follower(self, request, pk=None):
        try:
            follower = self.get_object()
            follower.delete()

            return Response({"message": "Follower deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete Follower: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_follower(self, request, pk=None):
        try:
            follower = self.get_object()
            serializer = self.get_serializer(follower, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Follower updated successfully",
                "follower": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to update Follower: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['post'], url_path='send')
    def send_message(self, request):
        try:
            data = request.data.copy()
            # Xử lý nếu có dữ liệu khác trong request
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Message sent successfully",
                "message_data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "error": f"Failed to send message: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_message(self, request, pk=None):
        try:
            message = self.get_object()
            message.delete()

            return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "error": f"Failed to delete message: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_message(self, request, pk=None):
        try:
            message = self.get_object()
            serializer = self.get_serializer(message, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Message updated successfully",
                "message_data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to update message: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MostFollowedArtistsView(APIView):
    """
    API để lấy danh sách nghệ sĩ được yêu thích nhất dựa trên số lượng người theo dõi.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Đếm số lượng người theo dõi cho mỗi nghệ sĩ
            artists = Artist.objects.annotate(follower_count=Count('follower')).order_by('-follower_count')

            # Serialize dữ liệu
            serializer = ArtistSerializer(artists, many=True)

            return Response({
                "message": "Most followed artists retrieved successfully",
                "artists": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve most followed artists: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
