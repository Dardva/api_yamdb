from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework import validators
from rest_framework_simplejwt.serializers import (
    PasswordField, TokenObtainPairSerializer)

from .constants import FORBIDDEN_USERNAME

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, attrs):
        if attrs['username'] in FORBIDDEN_USERNAME:
            raise validators.ValidationError('Недопустимое имя пользователя')
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=self.make_confirmation_code(validated_data)
        )
        return user

    def update(self, instance, validated_data):
        instance.password = self.make_confirmation_code(
            validated_data)
        instance.save()
        return instance

    def make_confirmation_code(self, data):
        confirmation_code = User.objects.make_random_password()
        self.send_confirmation_code(confirmation_code, data['email'])
        return make_password(confirmation_code)

    def send_confirmation_code(self, confirmation_code, email):
        send_mail(
            'Код подтверждения для Yamdb',
            f'Ваш код подтверждения: {confirmation_code}',
            '5hL7n@example.com',
            [email],
            fail_silently=False,
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения токена."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(
            write_only=True)
        self.fields['confirmation_code'] = PasswordField()
        del self.fields['password']

    def validate(self, attrs):

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['confirmation_code'],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
            
        except KeyError:
            pass
        self.user = authenticate(**authenticate_kwargs)
        if not self.user:
            raise serializers.ValidationError(
                'Пользователь с указанным кодом подтверждения не найден',
                code='authorization'
            )
        refresh = self.get_token(self.user)
        data = {'token': str(refresh), 'access': str(refresh.access_token)}
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['confirmation_code'] = user.password

        return token
