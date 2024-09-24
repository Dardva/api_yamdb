from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly, IsAuthorOrModeratorOrAdmin, IsOnlyAdmins
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    MyTokenObtainPairSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    UserMeSerializer,
    UserSerializer
)
from .viewsets import CreateListDestroyViewSet
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отзывов на произведения.
    Доступен для аутентифицированных пользователей.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)



class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для комментариев к отзывам.
    Доступен для аутентифицированных пользователей.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'delete', 'patch']


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOnlyAdmins]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


class UsersMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def get_object(self):
        return get_object_or_404(User, username=self.request.data['username'],
                                 email=self.request.data['email'])

    def create(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            instance = None
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
