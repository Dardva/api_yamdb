from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    MyTokenObtainPairView,
    RegisterView,
    UsersMeView,
    UsersViewSet
)

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/',
         MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', RegisterView.as_view(), name='signup'),
    path('v1/users/me/', UsersMeView.as_view(), name='users_me'),
    path('v1/', include(router.urls)),
]
