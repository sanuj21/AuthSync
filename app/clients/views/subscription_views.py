import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..serializers import SubscriptionSerializer
from ..models import Subscription
from ..permissions import isOwner

def generate_api_key():
    return uuid.uuid4().hex


# For Owner to manage Subscriptions
class SubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


#* --------------------------------------------- *#
