from django.urls import path
from .views import *

urlpatterns = [
    path('chatrooms/', UserChatRoomsView.as_view(), name='user-chatrooms'),
    path('chatrooms/<int:chatroom_id>/messages/', ChatRoomMessagesView.as_view(), name='chatroom-messages'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
]