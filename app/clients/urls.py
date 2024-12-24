from django.urls import path
from . import views
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def profileView(request, app_pk):
    return Response("Some", status=status.HTTP_200_OK)

urlpatterns = [
    path('', views.ClientAppListCreateView.as_view(), name='client_app_list_create'),

    # For Owner to retrieve, update, and delete a client app and its users
    path('<uuid:app_pk>/', views.ClientAppRetrieveUpdateDestroyView.as_view(), name='client_app_retrieve_update_destroy'),
    path('<uuid:app_pk>/users/', views.ClientUserListCreateView.as_view(), name='client_user_list_create'),
    path('<uuid:app_pk>/users/<uuid:user_pk>/', views.ClientUserRetrieveUpdateDestroyView.as_view(), name='client_user_retrieve_update_destroy'),

    # For Client User to register, login, update, reset password, and verify email
    path('<uuid:app_pk>/users/register/', views.ClientUserRegisterView.as_view(), name='client_user_register'),
    path('<uuid:app_pk>/users/login/', views.ClientUserLoginView.as_view(), name='client_user_login'),
    path('<uuid:app_pk>/users/my-profile/', views.ClientUserMyProfileView.as_view(), name='client_user_my_profile'),
    path('<uuid:app_pk>/users/update/<uuid:user_pk>/', views.ClientUserUpdateView.as_view(), name='client_user_updat'),
    path('<uuid:app_pk>/users/reset-password/<uuid:user_pk>/', views.ClientUserResetPasswordView.as_view(), name='client_user_reset_password'),
    path('<uuid:app_pk>/users/verify-email/<uuid:user_pk>/', views.ClientUserVerifyEmailView.as_view(), name='client_user_verify_email'),
]