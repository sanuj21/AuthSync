import uuid
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import ClientApp, ClientUser, Subscription


class ClientAPIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class to validate the Client-API-Key.
    """

    def authenticate(self, request):
        api_key = request.headers.get("api-key")

        # For Oauth
        if not api_key:
            state = request.GET.get('state')
            parsed_state = parse_qs(state)
            api_key = parsed_state.get('api_key', [None])[0]


        if not api_key:
            raise AuthenticationFailed("Client-API-Key is missing")

        try:
            subscription = Subscription.objects.get(api_key=api_key)
            if subscription.api_key_expires < now():
                raise AuthenticationFailed("Client-API-Key has expired")
        except ClientApp.DoesNotExist:
            raise AuthenticationFailed("Invalid Client-API-Key")

        # Attach the client_app object to the request for further use
        return (subscription, None)



# for Client User (Authorization Token Bug Fix)
class ClientUserJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        """
        Override authenticate to set request.client_user.
        """
        print(request.headers, 'request.headers')
        result = super().authenticate(request)
        if result is not None:
            user, token = result
            if isinstance(user, ClientUser):
                request.client_user = user  # Attach ClientUser to the request
            return user, token
        return None

    def get_user(self, validated_token):
        """
        Retrieve the ClientUser instance using the user_id from the token.
        """
        print(validated_token, 'validated_token')
        try:
            user_id = validated_token.get("user_id")
            # Convert the user_id to UUID
            user_id = uuid.UUID(user_id)
        except (ValueError, TypeError):
            raise AuthenticationFailed("Invalid user_id in token payload.")

        try:
            user = ClientUser.objects.get(id=user_id)
        except ClientUser.DoesNotExist:
            raise AuthenticationFailed("No ClientUser found for the given user_id.")

        if not user.is_active:
            raise AuthenticationFailed("ClientUser is inactive.")

        return user
