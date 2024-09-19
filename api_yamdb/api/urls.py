from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from .views import ReviewViewSet, CommentViewSet

# router = DefaultRouter()
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    # path('v1/', include(router.urls)),
]
