from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import (PasswordField,
                                                  TokenObtainPairSerializer)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя для админа."""

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
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if self.instance is not None:
            if 'email' in attrs and User.objects.filter(
                email=attrs['email']
            ).exclude(id=self.instance.id).exists():
                raise validators.ValidationError('Email уже зарегистрирован')
            if 'username' in attrs and User.objects.filter(
                username=attrs['username']
            ).exclude(id=self.instance.id).exists():
                raise validators.ValidationError(
                    'Username уже зарегистрирован')
        return attrs


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

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
        read_only_fields = ('role',)
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, attrs):
        if not self.instance:
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError(
                    'Email уже зарегистрирован')
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError(
                    'Username уже зарегистрирован')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.save()
        self.instance = user
        self.make_confirmation_code(validated_data)

        return user

    def update(self, instance, validated_data):
        self.make_confirmation_code(validated_data)
        return instance

    def make_confirmation_code(self, data):
        confirmation_code = default_token_generator.make_token(self.instance)
        self.send_confirmation_code(confirmation_code, data['email'])
        return make_password(confirmation_code)

    def send_confirmation_code(self, confirmation_code, email):
        send_mail(
            'Yamdb',
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
        if not User.objects.filter(
                username=attrs[self.username_field]).exists():
            raise Http404(
                'Пользователь с указанным именем не найден',
            )

        user = User.objects.get(username=attrs[self.username_field])
        if not default_token_generator.check_token(
            user, attrs['confirmation_code']
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения',
                code='authorization'
            )
        refresh = self.get_token(user)
        data = {'token': str(refresh.access_token)}
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token
