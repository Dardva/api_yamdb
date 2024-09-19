from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email',], name="%(app_label)s_%(class)s_unique")
        ]
