from django.db import models

from reviews.constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH


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
