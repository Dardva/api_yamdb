from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, mixins


from .serializers import (
    MyTokenObtainPairSerializer,
    SignupSerializer
)
User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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
        except Http404:
            return self.create(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(User, username=self.request.data['username'],
                                 email=self.request.data['email'])
