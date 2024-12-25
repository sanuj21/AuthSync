from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import ClientApp, ClientUser

class isOwner(BasePermission):
    """ Custom permission to only allow owners of an object to access or edit it """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


# class IsClientUserAuthenticated(BasePermission):
#     """
#     Custom permission to validate JWT for ClientUser.
#     """

#     def has_permission(self, request, view):
#         # Use SimpleJWT's authentication to decode the token
#         jwt_authenticator = JWTAuthentication()

#         try:
#             # Authenticate the token
#             validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split(' ')[1])
#             user = jwt_authenticator.get_user(validated_token)

#             # Check if the user is a ClientUser
#             if not isinstance(user, ClientUser):
#                 raise AuthenticationFailed('Not a valid ClientUser.')

#             # Attach the authenticated ClientUser to the request
#             request.client_user = user
#             return True

#         except Exception as e:
#             raise AuthenticationFailed(f'Authentication failed: {str(e)}')

#         return False
