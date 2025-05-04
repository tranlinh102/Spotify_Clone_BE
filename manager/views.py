from rest_framework import viewsets
from manager.models import (
    Playlist, Artist, ArtistSong, Album, Song, 
    Favorite, Download, AlbumSong, Follower, Message, PlaylistSong)
from .serializers import (
    PlaylistSerializer,ArtistSerializer, AlbumSongSerializer, 
    AlbumSerializer, SongSerializer, FavoriteSerializer, 
    DownloadSerializer, AlbumSongSerializer, FollowerSerializer, 
    MessageSerializer, ArtistSongSerializer, PlaylistSongSerializer, UserSerializer)
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
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # Action phân trang để lấy tất cả users
    @action(detail=False, methods=['get'], url_path='all-users')
    def get_all_users(self, request):
        # Lấy tất cả user và áp dụng phân trang
        users = User.objects.all()

        # Áp dụng phân trang
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Nếu không có phân trang thì trả thẳng
        serializer = self.get_serializer(users, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search_user(self, request):
        keyword = request.query_params.get('q', '').strip()
        if not keyword:
            return Response({'error': 'Thiếu tham số tìm kiếm "q"'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(
            Q(username__icontains=keyword) | Q(email__icontains=keyword)
        )

        # Áp dụng phân trang
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Nếu không có phân trang thì trả thẳng
        serializer = self.get_serializer(users, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='add')
    def create_user(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            is_active = request.data.get('is_active', True)
            is_staff = request.data.get('is_staff', False)
            is_superuser = request.data.get('is_superuser', False)

            # Kiểm tra bắt buộc
            if not username or not email or not password:
                return Response({'error': 'Username, Email và Mật khẩu là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username đã tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

            # Tạo user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = bool(int(is_active))
            user.is_staff = bool(int(is_staff))
            user.is_superuser = bool(int(is_superuser))
            user.save()

            serializer = self.get_serializer(user)
            return Response({'message': 'Tạo user thành công', 'user': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Lỗi tạo user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update')
    def update_user(self, request, pk=None):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Nếu có mật khẩu thì xử lý riêng để mã hóa
            password = serializer.validated_data.pop('password', None)
            user = serializer.save()
            if password:
                user.set_password(password)
                user.save()

            return Response({'message': 'Cập nhật user thành công', 'user': self.get_serializer(user).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Lỗi cập nhật user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_user(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_active = False
            user.save()
            return Response({'message': 'Đã vô hiệu hóa user'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Lỗi vô hiệu hóa user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='count')
    def count_users(self, request):
        try:
            total = User.objects.count()
            return Response({'total_users': total}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        try:
            user = self.get_object()
            new_password = request.data.get('password', '123456')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Đặt lại mật khẩu thành công'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Lỗi đặt lại mật khẩu: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [AllowAny]

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_S3_REGION_NAME', default='ap-southeast-1')
        )

    @action(detail=False, methods=['get'], url_path='count')
    def count_playlists(self, request):
        try:
            total_playlists = Playlist.objects.count()
            return Response({
                "message": "Total playlists count retrieved successfully",
                "total_playlists": total_playlists
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve playlists count: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_by_title(self, request):
        try:
            title_query = request.query_params.get('title', '').strip()
            if not title_query:
                return Response({"error": "Query parameter 'title' is required."}, status=status.HTTP_400_BAD_REQUEST)

            playlists = Playlist.objects.filter(title__icontains=title_query)
            serializer = self.get_serializer(playlists, many=True)
            return Response({
                "message": "Search results",
                "results": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to search playlists: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
   
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

    # Action phân trang để lấy tất cả artist
    @action(detail=False, methods=['get'], url_path='all-artists')
    def get_all_artists(self, request):
        artists = Artist.objects.all()

        # Áp dụng phân trang
        page = self.paginate_queryset(artists)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Nếu không có phân trang thì trả thẳng
        serializer = self.get_serializer(artists, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='top-followed')
    def top_followed_artists(self, request):
        try:
            top_artists = Artist.objects.annotate(
                follower_count=Count('follower')
            ).order_by('-follower_count')

            serializer = self.get_serializer(top_artists, many=True)
            return Response({
                "message": "Top followed artists retrieved successfully",
                "artists": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve top followed artists: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    @action(detail=False, methods=['get'], url_path='search')
    def search_artist(self, request):
        try:
            name_query = request.query_params.get('name', '').strip()
            if not name_query:
                return Response({"error": "Query parameter 'name' is required."}, status=status.HTTP_400_BAD_REQUEST)

            artists = Artist.objects.filter(name__icontains=name_query).order_by('artist_id')

            # Phân trang kết quả tìm kiếm
            page = self.paginate_queryset(artists)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # Nếu không phân trang được (hiếm khi xảy ra)
            serializer = self.get_serializer(artists, many=True)
            return Response({
                "message": "Search results",
                "results": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to search artists: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    # Action phân trang để lấy tất cả album
    @action(detail=False, methods=['get'], url_path='all-albums')
    def get_all_albums(self, request):
        albums = Album.objects.all()

        # Áp dụng phân trang
        page = self.paginate_queryset(albums)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Nếu không có phân trang thì trả thẳng
        serializer = self.get_serializer(albums, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='count')
    def count_album(self, request):
        try:
            total_albums = Album.objects.count()
            return Response({
                "message": "Total albums count retrieved successfully",
                "total_albums": total_albums
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve album count: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            if image_file and album.image and album.image.name:
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

    @action(detail=False, methods=['get'], url_path='search')
    def search_album(self, request):
        try:
            title_query = request.query_params.get('title', '').strip()

            # Tìm album theo tiêu đề
            queryset = Album.objects.filter(title__icontains=title_query).order_by('album_id')

            # Áp dụng phân trang
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            # Nếu không có trang nào (dữ liệu rỗng)
            serializer = self.get_serializer(queryset, many=True)
            return Response({"results": serializer.data, "count": len(serializer.data)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Failed to search albums: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    @action(detail=False, methods=['get'], url_path='top-favourite')
    def top_favorite_songs(self, request):
        try:
            top_songs = (
                Song.objects.annotate(favorite_count=Count('favorite'))
                .order_by('-favorite_count')[:10]  # Lấy top 10 bài hát
            )
            serializer = self.get_serializer(top_songs, many=True)
            return Response({
                "message": "Top favorite songs retrieved successfully",
                "songs": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve top favorite songs: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='count')
    def count_song(self, request):
        try:
            total_songs = Song.objects.count()
            return Response({
                "message": "Total songs count retrieved successfully",
                "total_songs": total_songs
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve song count: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    @action(detail=False, methods=['get'], url_path='search')
    def search_song(self, request):
        try:
            title_query = request.query_params.get('title', '').strip()
            if not title_query:
                return Response(
                    {"error": "Query parameter 'title' is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            songs = Song.objects.filter(title__icontains=title_query)
            serializer = self.get_serializer(songs, many=True)
            return Response({
                "message": "Search results",
                "results": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to search songs: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ArtistSongViewSet(viewsets.ModelViewSet):
    queryset = ArtistSong.objects.all()
    serializer_class = ArtistSongSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def get_queryset(self):
        album_id = self.request.query_params.get('album_id')
        if album_id:
            return AlbumSong.objects.filter(album_id=album_id)
        return AlbumSong.objects.all()
    
    @action(detail=False, methods=['get'], url_path='not-in-album-by-artist')
    def get_songs_not_in_album_but_by_album_artist(self, request):
        album_id = request.query_params.get('album_id')
        if not album_id:
            return Response({"error": "album_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Bước 1: Lấy các song_id trong album
            album_song_ids = AlbumSong.objects.filter(album_id=album_id).values_list('song_id', flat=True)

            # Bước 2: Lấy artist_id của album
            album = Album.objects.get(album_id=album_id)
            artist_id = album.artist_id  # giả sử Album có khóa ngoại: artist = models.ForeignKey(Artist, ...)

            # Bước 3: Lấy tất cả bài hát của artist
            artist_song_ids = ArtistSong.objects.filter(artist_id=artist_id).values_list('song_id', flat=True).distinct()

            # Bước 4: Loại bỏ bài hát đã thuộc album
            result_song_ids = list(set(artist_song_ids) - set(album_song_ids))

            # Bước 5: Lấy dữ liệu bài hát
            songs = Song.objects.filter(song_id__in=result_song_ids)

            from .serializers import SongSerializer
            serializer = SongSerializer(songs, many=True)

            return Response({
                "message": "Songs by album's artist but not in album retrieved successfully",
                "songs": serializer.data
            }, status=status.HTTP_200_OK)

        except Album.DoesNotExist:
            return Response({"error": "Album not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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



# Create your views here.
