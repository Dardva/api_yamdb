from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=(
            ('user', 'user'),
            ('moderator', 'moderator'),
            ('admin', 'admin'),
        ),
        default='user'
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
