# from rest_framework import viewsets
# # from rest_framework.pagination import PageNumberPagination
# from django.shortcuts import get_object_or_404

# from reviews.models import Title, Review, Comment
# from .serializers import ReviewSerializer, CommentSerializer
# # from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly


# class ReviewViewSet(viewsets.ModelViewSet):
#     """
#     Вьюсет для обработки операций с отзывами.
#     """
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly]
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         return Review.objects.filter(title_id=self.kwargs.get('title_id'))

#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         serializer.save(author=self.request.user, title=title)


# class CommentViewSet(viewsets.ModelViewSet):
#     """
#     Вьюсет для обработки операций с комментариями.
#     """
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly]
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         return Comment.objects.filter(
#             review_id=self.kwargs.get('review_id'),
#             review__title_id=self.kwargs.get('title_id')
#         )

#     def perform_create(self, serializer):
#         review = get_object_or_404(
#             Review,
#             pk=self.kwargs.get('review_id'),
#             title_id=self.kwargs.get('title_id')
#         )
#         serializer.save(author=self.request.user, review=review)
