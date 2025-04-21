from django.shortcuts import render, get_object_or_404
import boto3
from django.conf import settings
from decouple import config
from django.db.models import F

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from music.models import Songs
from music.serializers import SongsSerializer

class SongUploadView(APIView):
    def post(self, request):
        serializer = SongsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Song uploaded successfully",
                "song": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongListView(ListAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

class SongDeleteView(APIView):
    def delete(self, request, song_id):
        # Lấy bài hát từ cơ sở dữ liệu
        song = get_object_or_404(Songs, song_id=song_id)
        
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
    serializer_class = SongsSerializer

    def get_queryset(self):
        return Songs.objects.order_by(F('created_at').desc(nulls_last=True))[:8]