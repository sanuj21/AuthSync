import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now, timedelta
from django.contrib.auth.hashers import make_password, check_password

from .models import ClientApp, ClientUser
from .serializers import ClientAppSerializer, ClientUserSerializer
from .permissions import isOwner
from .authentications import ClientAPIKeyAuthentication, ClientUserJWTAuthentication

def generate_api_key():
    return uuid.uuid4().hex

class ClientAppListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ClientApp.objects.all()
    serializer_class = ClientAppSerializer
    """Customizing the create method to generate an API key and set the expiry date"""

    def perform_create(self, serializer):
        user = self.request.user
        day_count = self.request.data.get('day_count')

        # Validate day_count
        try:
            day_count = int(day_count)
            if day_count <= 0:
                raise ValueError("Day count must be a positive integer.")
        except (ValueError, TypeError):
            raise ValidationError({"day_count": "Invalid or missing day_count. Must be a positive integer."})

        serializer.save(
            owner=user,
            api_key=generate_api_key(),
            api_key_expires=now() + timedelta(days=day_count)
        )

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
    authentication_classes = [ClientAPIKeyAuthentication]

    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    # Restricting access to the client user details to if api key is invalid, key will be passed in the header
    def get_queryset(self):
        api_key = self.request.headers.get('api-key')
        return self.queryset.filter(client_app__api_key=api_key)

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
    authentication_classes = [ClientAPIKeyAuthentication]

    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    # Restricting access to the client user details to if api key is valid, key will be passed in the header
    def get_queryset(self):
        api_key = self.request.headers.get('api-key')
        return self.queryset.filter(client_app__api_key=api_key)



# Views for Client User actions

class ClientUserRegisterView(generics.CreateAPIView):

    authentication_classes = [ClientAPIKeyAuthentication]

    query_set = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    # Customizing create method to set the client app based on the api key and set the password if login type is Email
    def perform_create(self, serializer):
        # client_app = ClientApp.objects.get(api_key=api_key)
        app_pk = self.kwargs.get('app_pk')
        client_app = ClientApp.objects.get(id=app_pk)
        login_type = self.request.data.get('login_type')

        # set the client app to reference the client user
        serializer.save(client_app=client_app)

        if login_type is None: # if login type is not provided, set it to Email
            password = self.request.data.get('password')
            if not password:
                raise ValidationError({"password": "Password is required for Email login type."})

            # hash the password
            print("hashed password", make_password(password))
            serializer.save(password=make_password(password))



class ClientUserLoginView(generics.GenericAPIView):

    authentication_classes = [ClientAPIKeyAuthentication]

    query_set = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            client_user = ClientUser.objects.get(email=email)
        except ClientUser.DoesNotExist:
            raise ValidationError({"email": "Invalid email or password."})

        if not check_password(password, client_user.password):
            raise ValidationError({"email": "Invalid email or password."})

        # Generate JWT token
        refresh = RefreshToken.for_user(client_user)
        access_token = refresh.access_token

        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
        }, status=status.HTTP_200_OK)



class ClientUserMyProfileView(generics.GenericAPIView):
    authentication_classes = [ClientUserJWTAuthentication]

    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    def post(self, request, *args, **kwargs):
        client_user = request.client_user
        serializer = self.serializer_class(client_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientUserUpdateView(generics.GenericAPIView):
    pass


class ClientUserResetPasswordView(generics.GenericAPIView):
    pass

class ClientUserVerifyEmailView(generics.GenericAPIView):
    pass

