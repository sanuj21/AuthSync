from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from clients.models import ApiPlan
from clients.serializers import ApiPlanSerializer


class RegisterUserView(generics.CreateAPIView):
    """"API View for registering a user"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class PlanListView(generics.ListAPIView):
    """"API View for listing plans"""
    queryset = ApiPlan.objects.all()
    serializer_class = ApiPlanSerializer