from django.urls import path
from .views import CookieTokenRefreshView, LogoutView, RegisterView, LoginView, UserInfoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh_cookie'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('userInfo/', UserInfoView.as_view(), name='user-info'),
]