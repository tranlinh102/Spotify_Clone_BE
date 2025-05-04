from django.urls import path
from .views import UserChatRoomsView

urlpatterns = [
    path('chatrooms/', UserChatRoomsView.as_view(), name='user-chatrooms'),
]