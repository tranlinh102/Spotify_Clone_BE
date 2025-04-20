from django.shortcuts import render, get_object_or_404

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
        song = get_object_or_404(Songs, song_id=song_id)
        song.delete()
        return Response({"message": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
