from django.urls import include, path
from users.views import MyTokenObtainPairView, RegisterView
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet)
from users.views import UsersViewSet

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
    path('v1/', include(router.urls)),
]
