from django.core import validators
from django.utils.deconstruct import deconstructible

from .constants import FORBIDDEN_USERNAME


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = 'Недопустимое имя пользователя.'
    flags = 0

    def __call__(self, value):
        super().__call__(value)
        if value in FORBIDDEN_USERNAME:
            raise validators.ValidationError('Недопустимое имя пользователя.')
