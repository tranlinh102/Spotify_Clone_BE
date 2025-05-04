from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from manager.models import ChatRoom
from manager.serializers import ChatRoomWithLastMessageSerializer

class UserChatRoomsView(APIView):
    def get(self, request):
        user = request.user

        # Lấy tất cả ChatRoom mà người dùng tham gia
        chatrooms = ChatRoom.objects.filter(
            models.Q(user1=user) | models.Q(user2=user)
        ).annotate(
            last_message_timestamp=models.Max('chatmessage__timestamp')
        ).order_by('-last_message_timestamp')

        # Serialize dữ liệu
        serializer = ChatRoomWithLastMessageSerializer(chatrooms, many=True, context={'request': request})
        return Response(serializer.data)