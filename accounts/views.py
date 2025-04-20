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
    
def set_jwt_cookies(response: Response, access_token: str, refresh_token: str = None):
    # ACCESS TOKEN – gửi mọi request
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=False,
        secure=True,
        samesite='None',
        path='/',
        max_age=60 * 30 # 30 phút
    )

    # REFRESH TOKEN – dùng riêng, nếu có truyền vào
    if refresh_token:
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/api/auth/refresh',
            max_age=7 * 24 * 60 * 60  # 7 ngày
        )

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        res = Response({
            'message': 'Login success', 
            'is_staff': serializer.user.is_staff, 
            'access_token': access #Lấy thêm access token để gửi về client
            }, status=status.HTTP_200_OK)
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