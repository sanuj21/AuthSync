
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password

from ..models import ClientApp, ClientUser, ClientUserCustomField, Subscription
from ..serializers import ClientUserSerializer
from ..authentications import ClientAPIKeyAuthentication, ClientUserJWTAuthentication


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

        # Checking if no_of_users is less than max_users
        subs_plan = Subscription.objects.get(client_app=client_app)
        if client_app.no_of_users >= subs_plan.plan.max_users:
            raise ValidationError({"max_users": "Maximum number of users reached."})


        login_type = self.request.data.get('login_type')
        # set the client app to reference the client user
        serializer.save(client_app=client_app)

        User_Fields = [f.name for f in ClientUser._meta.get_fields()]
        # find all the key which are not in user model, and put them in ClientUserCustomField model
        for key in self.request.data:
            if key not in User_Fields:
                # create a custom field
                ClientUserCustomField.objects.create(
                    user=serializer.instance,
                    key=key,
                    value=self.request.data[key]
                )

        if login_type is None: # if login type is not provided, set it to Email
            password = self.request.data.get('password')
            if not password:
                raise ValidationError({"password": "Password is required for Email login type."})

            # hash the password
            serializer.save(password=make_password(password))


        # Increase the user count in the ClientApp
        client_app.no_of_users += 1
        client_app.save()




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
    authentication_classes = [ClientUserJWTAuthentication, ClientAPIKeyAuthentication]

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

