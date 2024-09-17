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
    genre = models.ForeignKey(
        Genre, verbose_name='Жанр', on_delete=models.CASCADE)
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
    Модель отзыва.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ]
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author} на "{self.title}"'


class Comment(models.Model):
    """
    Модель комментария.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Комментарий от {self.author} к отзыву {self.review}'

