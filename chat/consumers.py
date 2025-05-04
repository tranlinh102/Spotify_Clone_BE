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

    async def receive(self, text_data=None, bytes_data=None):
        # Nhận tin nhắn từ WebSocket client
        data = json.loads(text_data)
        message = data.get('message')
        recipient_id = data.get('recipient_id')  # ID của người nhận
        room_id = data.get('room_id')  # ID của phòng (nếu có)

        try:
            sender = self.scope['user']

            chatroom_data = {
                'id': room_id,
                'user1_id': sender.id,
                'user2_id': recipient_id
            }

            # Kiểm tra xem phòng chat đã tồn tại chưa, nếu chưa thì tạo mới
            if not room_id:
                chatroom = await save_serializer(ChatRoomSerializer, chatroom_data)
                room_id = chatroom.id

            message_data = {
                'sender_id': sender.id,
                'chatroom_id': room_id,
                'content': message
            }

            await save_serializer(ChatMessageSerializer, message_data)

            # Gửi tin nhắn đến group
            await self.channel_layer.group_send(
                f"user_{recipient_id}",
                {
                    "type": "chat_message",
                    "message": message,
                    "sender_id": sender.id,
                    "room_id": room_id  # ID của phòng chat
                }
            )

            await self.send(text_data=json.dumps({
                "status": "success",
                "message": "Message sent successfully",
                "room_id": room_id  # ID của phòng chat
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                "status": "error",
                "message": f"Failed to send message: {str(e)}"
            }))


    async def chat_message(self, event):
        # Nhận tin nhắn từ group và gửi đến WebSocket client
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            "message": message,
            "sender_id": sender_id
        }, ensure_ascii=False))