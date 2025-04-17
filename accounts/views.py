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

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        res = Response({'message': 'Login success'}, status=status.HTTP_200_OK)
        res.data['is_staff'] = serializer.user.is_staff

        # REFRESH TOKEN: HttpOnly cookie
        res.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='None',  # SameSite=None để cookie có thể gửi đến các domain khác
            path='/api/auth/refresh',  # chỉ gửi ở endpoint refresh
            max_age=7 * 24 * 60 * 60 # 7 ngày
        )

        # ACCESS TOKEN: Normal Cookie → frontend sẽ tự gửi cùng mọi request
        res.set_cookie(
            key='access_token',
            value=access,
            httponly=False,
            secure=True,
            samesite='None',  # SameSite=None để cookie có thể gửi đến các domain khác
            path='/',
            max_age=60  # 5 phút
        )

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
            res = Response({'Refresh access_token success': access_token}, status=status.HTTP_200_OK)

            # Lưu access token mới vào cookie thường (frontend sẽ tự gửi kèm)
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=False,
                secure=True,
                samesite='None',  # SameSite=None để cookie có thể gửi đến các domain khác
                path='/',
                max_age=60  # 5 phút
            )

            return res

        except TokenError as e:
            return Response(
                {'detail': 'Invalid or expired refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        res.delete_cookie(
            key='access_token',
            path='/',
        )
        res.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],  # refresh_token
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        )
        res = Response({"message": "Logout success"}, status=status.HTTP_200_OK)
        return res
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff
        })