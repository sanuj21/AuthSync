from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    """"API View for registering a user"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
