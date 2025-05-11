from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from manager.models import ChatMessage, ChatRoom
from django.contrib.auth.models import User
from manager.serializers import ChatMessageSerializer, ChatRoomWithLastMessageSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    
class ChatRoomMessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user
        chatroom_id = self.kwargs.get('chatroom_id')

        # Kiểm tra xem người dùng có tham gia ChatRoom không
        chatroom = ChatRoom.objects.filter(
            models.Q(user1=user) | models.Q(user2=user),
            id=chatroom_id
        ).first()

        if not chatroom:
            return ChatMessage.objects.none()  # Trả về queryset rỗng nếu không có quyền truy cập

        # Lấy tất cả tin nhắn của ChatRoom
        return ChatMessage.objects.filter(chatroom=chatroom)
    
class SendMessageView(APIView):

    def options(self, request, *args, **kwargs):
        return Response({'detail': 'Method "OPTIONS" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        user = request.user
        data = request.data

        recipient_id = data.get('recipient_id')
        content = data.get('content')
        chatroom_id = data.get('chatroom_id')

        if not recipient_id or not content:
            return Response({"error": "recipient_id and content are required."}, status=400)

        # Xử lý phòng chat
        if chatroom_id:
            try:
                chatroom = ChatRoom.objects.get(id=chatroom_id)
            except ChatRoom.DoesNotExist:
                return Response({"error": "ChatRoom not found."}, status=404)
        else:
            # Tạo mới chatroom nếu chưa có
            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                return Response({"error": "Recipient user not found."}, status=404)

            user1, user2 = sorted([user, recipient], key=lambda u: u.id)

            chatroom, _ = ChatRoom.objects.get_or_create(user1=user1, user2=user2)

        # Tạo tin nhắn mới
        message_data = {
            'sender_id': user.id,
            'chatroom_id': chatroom.id,
            'content': content
        }

        serializer = ChatMessageSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()

            # Gửi real-time qua WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{recipient_id}",
                {
                    "type": "chat_message",
                    "message": content,
                    "sender_id": user.id,
                    "room_id": chatroom.id,
                    "timestamp": message.timestamp.isoformat(),
                }
            )

            # Trả về cả chatroom_id và recipient_id
            response_data = serializer.data
            response_data["chatroom_id"] = chatroom.id
            response_data["recipient_id"] = recipient_id

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)