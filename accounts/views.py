from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from decouple import config

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token
    
def set_jwt_cookies(response: Response, access_token: str, refresh_token: str = None):
    # ACCESS TOKEN – gửi mọi request
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=False,
        secure=config('COOKIE_SECURE', default=True, cast=bool),
        samesite=config('COOKIE_SAMESITE', default='None'),
        path='/',
        max_age=60 * 60 # 60 phút
    )

    # REFRESH TOKEN – dùng riêng, nếu có truyền vào
    if refresh_token:
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=config('COOKIE_SECURE', default=True, cast=bool),
            samesite=config('COOKIE_SAMESITE', default='None'),
            path='/api/auth/',
            max_age=7 * 24 * 60 * 60  # 7 ngày
        )

def get_user_info(user):
    # try:
    #     profile = user.profile  # OneToOneField -> Django tự tạo `user.profile`
    #     avatar = profile.avatar
    #     favorite_books = profile.favorite_books
    # except Profile.DoesNotExist:
    #     avatar = None
    #     favorite_books = None

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        # "avatar": avatar,
        # "favorite_books": favorite_books,
    }

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        res = Response({'message': 'Login success', 'is_staff': serializer.user.is_staff, 'access token': access, 'user_info': get_user_info(serializer.user)}, status=status.HTTP_200_OK)
        set_jwt_cookies(res, access_token=access, refresh_token=refresh)
        return res

class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token not found in cookie'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Tạo access token mới từ refresh
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            # Tạo response
            res = Response({'message': "Refresh access_token success"}, status=status.HTTP_200_OK)
            set_jwt_cookies(res, access_token=access_token)  # không cần set lại refresh

            return res

        except TokenError as e:
            return Response(
                {'detail': 'Invalid or expired refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        res = Response({"message": "Logout success"}, status=status.HTTP_200_OK)  # 🛠 Khởi tạo res trước
        res.delete_cookie(
            key='access_token',
            path='/',
            samesite=config('COOKIE_SAMESITE', default='None'),
        )
        res.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],  # refresh_token
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            samesite=config('COOKIE_SAMESITE', default='None'),
        )
        return res


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'user_info': get_user_info(user)}, status=status.HTTP_200_OK)
    
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "674163388601-d7dk6m8us1j3duai1cp1ipejcoce3339.apps.googleusercontent.com")
            email = idinfo['email']
            name = idinfo.get('name', '')
            
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email, defaults={'username': name, 'email': email})
            
            # Tạo token JWT
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Tạo response giống LoginView
            res = Response({
                "message": "Login success",
                "is_staff": user.is_staff,
                "access token": str(access),
                "user_info": get_user_info(user)
            }, status=status.HTTP_200_OK)

            # Set cookie nếu bạn dùng kiểu này
            set_jwt_cookies(res, access_token=access, refresh_token=refresh)

            return res
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)