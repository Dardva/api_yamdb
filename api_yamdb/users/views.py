from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsOnlyAdmins
from .serializers import (MyTokenObtainPairSerializer, SignupSerializer,
                          UserMeSerializer, UserSerializer)

User = get_user_model()


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
        return User.objects.get(username=self.request.user)


class RegisterView(
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Exception:
            response = self.create(request, *args, **kwargs)
            response.status_code = 200
            return response
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(User, username=self.request.data['username'],
                                 email=self.request.data['email'])
