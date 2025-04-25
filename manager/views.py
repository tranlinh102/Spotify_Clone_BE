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


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    @action (detail=False, methods=['post'], url_path='add')
    def add_playlist(self, request, *args, **kwargs):
        try:
            #Lấy dữ liệu từ request
            data = request.data
            image_file = request.FILES.get('image')
            if image_file:
                # Upload file lên S3
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key= config('AWS_SECRET_ACCESS_KEY'),
                    region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
                )
                bucket_name = config('AWS_STORAGE_BUCKET_NAME')
                # Tạo đường dẫn cho file trên S3
                file_path = f'playlists/{image_file.name}'
                try:
                    # Upload file lên S3
                    s3.upload_fileobj(image_file, bucket_name, file_path)
                    image_url = f'https://{bucket_name}.s3.amazonaws.com/{file_path}'
                except (NotADirectoryError, PartialCredentialsError) as e:
                    return Response({"error": f"Failed to upload file to S3: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    return Response({"error": f"Failed to upload file to S3: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                image_url = None
            
            #Lưu playlist vào cơ sở dữ liệu
            data['image'] = image_url
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)
            return Response({
                "message": "Playlist created successfully",
                "playlist": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create playlist: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

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
            album.delete()  # Django sẽ tự xóa file khỏi S3 nếu cấu hình đúng
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

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

    

class ArtistSongViewSet(viewsets.ModelViewSet):
    queryset = ArtistSong.objects.all()
    serializer_class = ArtistSongSerializer

class PlaylistSongViewSet(viewsets.ModelViewSet):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer

class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = AlbumSong.objects.all()
    serializer_class = AlbumSongSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class DownloadViewSet(viewsets.ModelViewSet):
    queryset = Download.objects.all()
    serializer_class = DownloadSerializer

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# Create your views here.
