from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.db import IntegrityError
from django.core.mail import send_mail

from .constants import FORBIDDEN_USERNAME

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""
    confirmation_code = serializers.SlugRelatedField(
        slug_field='password', read_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'confirmation_code', )

    def validate(self, attrs):
        if attrs['username'] in FORBIDDEN_USERNAME:
            self.fail('invalid_username')
        return attrs

    def create(self, validated_data):
        user = User.objects.get_or_create(validated_data)
        confirmation_code = User.objects.make_random_password()
        validated_data['confirmation_code'] = make_password(confirmation_code)
        try:
            user = user.update_or_create(validated_data)
            print(user)
        except IntegrityError:
            self.fail("cannot_create_user")
        self.send_confirmation_code(validated_data, confirmation_code)
        return user

    def send_confirmation_code(self, data, confirmation_code=None):
        send_mail(
            'Код подтверждения для Yamdb',
            f'Ваш код подтверждения: {confirmation_code}',
            '5hL7n@example.com',
            [data['email']],
            fail_silently=False,
        )
