from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        
        # Kiểm tra email trùng
        try:
            existing_user = User.objects.get(email=email)
            if existing_user.password:  # đã có mật khẩu thì không cho đăng ký lại
                raise serializers.ValidationError({'email': 'Email đã được đăng ký với tài khoản có mật khẩu.'})
            else:
                # Cập nhật thông tin cho user có sẵn nhưng chưa có password
                existing_user.username = username
                existing_user.set_password(password)
                existing_user.save()
                return existing_user
        except User.DoesNotExist:
            # Email chưa tồn tại → tạo mới user
            user = User.objects.create_user(**validated_data)
            return user
