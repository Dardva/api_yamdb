from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api.viewsets import CreateListDestroyViewSet
from api.permissions import IsAdminOrReadOnly, IsAuthorOrModeratorOrAdmin


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отзывов на произведения.
    Доступен для аутентифицированных пользователей.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_queryset(self):
        """
        Получает список отзывов для определённого произведения.
        """
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """
        Создаёт новый отзыв и обновляет рейтинг произведения.
        """
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        self.update_title_rating(title)

    def update_title_rating(self, title):
        """
        Обновляет средний рейтинг произведения на основе отзывов.
        """
        reviews = title.reviews.all()
        rating = reviews.aggregate(models.Avg('score'))['score__avg']
        title.rating = rating
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для комментариев к отзывам.
    Доступен для аутентифицированных пользователей.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_queryset(self):
        """
        Получает список комментариев для определённого отзыва.
        """
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Создаёт новый комментарий к отзыву.
        """
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "PUT method is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
