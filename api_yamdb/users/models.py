from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator


class User(AbstractUser):
    """Модель пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    bio = models.TextField(verbose_name='Биография',
                           blank=True, max_length=500)
    role = models.CharField(
        max_length=10,
        choices=(
            (USER, 'user'),
            (MODERATOR, 'moderator'),
            (ADMIN, 'admin'),
        ),
        default='user'
    )
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        verbose_name='Имя пользователя', max_length=150, unique=True,
        help_text=(
            'Required. 150 characters or fewer.',
            'Letters, digits and @/./+/-/_ only.'),
        validators=[UsernameValidator()],)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
