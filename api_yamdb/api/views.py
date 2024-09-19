from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
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
# from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки операций с отзывами.
    """
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly]
    pagination_class = PageNumberPagination

#     def get_queryset(self):
#         return Review.objects.filter(title_id=self.kwargs.get('title_id'))

#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки операций с комментариями.
    """
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly]
    pagination_class = PageNumberPagination

#     def get_queryset(self):
#         return Comment.objects.filter(
#             review_id=self.kwargs.get('review_id'),
#             review__title_id=self.kwargs.get('title_id')
#         )

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAdminUser]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request):
        return Response(
            {"detail": "PUT method is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
