from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class JWTWebsocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Lấy cookie từ headers
        headers = dict(scope['headers'])
        cookie_header = headers.get(b'cookie', b'').decode()
        cookies = {key.strip(): value.strip() for key, value in (item.split('=') for item in cookie_header.split(';') if '=' in item)}

        # Lấy access_token từ cookie
        access_token = cookies.get('access_token')

        if access_token:
            try:
                # Xác thực token và lấy user_id
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = await sync_to_async(User.objects.get)(id=user_id)
                scope['user'] = user
            except Exception as e:
                scope['user'] = AnonymousUser()
        else:
            print("No access token found")
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)