
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import parse_qs
from rest_framework.views import APIView
from ..services.oauth_service import createJwtToken
from ..utils import load_settings_from_db
from ..models import ClientApp, ClientUser, ClientUserCustomField, Subscription
from ..serializers import ClientUserSerializer, OAuthSerializer
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


# Login in client user via Oauth
class ClientUserGoogleLoginView(APIView):

    authentication_classes = [ClientAPIKeyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        # Loading the Oauth Keys
        state = request.GET.get('state')
        parsed_state = parse_qs(state)
        client_app_id = parsed_state.get('client_app_id')[0]
        load_settings_from_db(client_app_id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth_serializer = OAuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)

        validated_data = auth_serializer.validated_data
        user_data, access_token, refresh = createJwtToken(validated_data)
        response = redirect(settings.CLIENT_APP_SETTINGS['BASE_APP_URL'])
        response.set_cookie('access_token', access_token, max_age = 60 * 24 * 60 * 1) # 1 day
        response.set_cookie('refresh_token', str(refresh), max_age = 60 * 24 * 60 * 60) # 60 days

        return response

    def post(self, request, *args, **kwargs):
        pass

# End of Oauth login


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

