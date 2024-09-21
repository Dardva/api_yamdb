from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.contrib.auth import get_user_model

from reviews.constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('Слаг', unique=True, max_length=MAX_SLUG_LENGTH)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('Слаг', unique=True, max_length=MAX_SLUG_LENGTH)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    year = models.IntegerField('Год создания')
    rating = models.IntegerField('Рейтинг')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'titles'
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

    @property
    def rating(self):
        """
        Вычисляет средний рейтинг произведения.
        """
        return self.reviews.aggregate(Avg('score'))['score__avg']


class Review(models.Model):
    """
    Модель отзыва на произведение.
    Один пользователь может оставить только один отзыв на произведение.
    """

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            )
        ]
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """
    Модель комментария к отзыву.
    """

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[:50]
