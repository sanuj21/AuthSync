
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from ..models import ClientApp, ClientUser
from ..permissions import isOwner
from ..serializers import ClientUserSerializer, ClientAppSerializer

class ClientAppListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ClientApp.objects.all()
    serializer_class = ClientAppSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):
        # Filter ClientApps to only those owned by the authenticated user
        return ClientApp.objects.filter(owner=self.request.user)



class ClientAppRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = ClientApp.objects.all()
    serializer_class = ClientAppSerializer

    # Restricting access to the client app details to the owner of the app
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)


class ClientUserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    # Restricting access to the client user details to the owner of the app
    def get_queryset(self):
        app_pk = self.kwargs.get('app_pk')
        return self.queryset.filter(client_app__id=app_pk)

    # Customizing create method to set the client app based on the api key and set the password if login type is Email
    def perform_create(self, serializer):
        # client_app = ClientApp.objects.get(api_key=api_key)
        app_pk = self.kwargs.get('app_pk')
        client_app = ClientApp.objects.get(id=app_pk)
        login_type = self.request.data.get('login_type')
        password = self.request.data.get('password')

        if login_type == 'Email' and not password:
            raise ValidationError({"password": "Password is required for Email login type."})

        # set the client app to reference the client user
        serializer.save(client_app=client_app)

        # hash the password
        serializer.save(password=make_password(password))



class ClientUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer
    # lookup_field = 'id'

    # Restricting access to the client user details to the owner of the app
    def get_queryset(self):
        app_pk = self.kwargs.get('app_pk')
        return self.queryset.filter(client_app__id=app_pk)

