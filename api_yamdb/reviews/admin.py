from django.contrib import admin
from .models import Category, Genre, Title, Review, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'display_genres', 'rating',)
    search_fields = ('name', 'category__name', 'genre__name',)
    list_filter = ('year', 'category', 'genre',)
    ordering = ('name',)
    raw_id_fields = ('category',)
    filter_horizontal = ('genre',)

    def display_genres(self, obj):
        """Отображает жанры произведения в виде строки."""
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genres.short_description = 'Жанры'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date',)
    search_fields = ('title__name', 'author__username', 'text',)
    list_filter = ('score', 'pub_date',)
    ordering = ('-pub_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'pub_date',)
    search_fields = ('review__text', 'author__username', 'text',)
    list_filter = ('pub_date',)
    ordering = ('-pub_date',)
