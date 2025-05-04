from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from manager.serializers import ChatMessageSerializer, ChatRoomSerializer, save_serializer
import json

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lấy thông tin người dùng hiện tại
        user = self.scope['user']
        if user.is_authenticated:
            # Tạo group dựa trên ID người dùng
            self.room_group_name = f"user_{user.id}"

            # Thêm người dùng vào group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Chấp nhận kết nối WebSocket
            await self.accept()
        else:
            # Từ chối kết nối nếu người dùng chưa đăng nhập
            await self.close()

    async def disconnect(self, code):
        # Xóa người dùng khỏi group khi ngắt kết nối
        user = self.scope['user']
        if user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        room_id = data['room_id']

        # Gửi tin nhắn đến group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
                "room_id": room_id,
            }
        )

    async def chat_message(self, event):
        # Gửi tin nhắn đến WebSocket client
        await self.send(text_data=json.dumps({
            "message": event['message'],
            "sender_id": event['sender_id'],
            "room_id": event['room_id'],
        }, ensure_ascii=False))