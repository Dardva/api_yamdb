from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import filters, generics, permissions, viewsets
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
