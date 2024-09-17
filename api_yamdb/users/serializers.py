from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.db import IntegrityError
from constants import FORBIDDEN_USERNAME
User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""
    password = serializers.CharField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'password', )

    def validate(self, attrs):
        if attrs['username'] in FORBIDDEN_USERNAME:
            self.fail('invalid_username')
        return attrs

    def create(self, validated_data):
        password = User.objects.make_random_password()
        validated_data['password'] = make_password(password)
        try:
            user = User.objects.update_or_create(validated_data)
            print(user)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user
