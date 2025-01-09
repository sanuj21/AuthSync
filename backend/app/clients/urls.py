from django.urls import path
from .views import subscription_views, user_views, client_user_views
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view

@api_view(['GET'])
def healthCheck(request):
    print(settings.BASE_API_URL)
    return Response({"message": "Hello, World!"})


urlpatterns = [
    path('', user_views.ClientAppListCreateView.as_view(), name='client_app_list_create'),

    path('health-check/', healthCheck, name='health_check'),

    # For Owner to retrieve, update, and delete a client app and its users
    path('<uuid:app_pk>/', user_views.ClientAppRetrieveUpdateDestroyView.as_view(), name='client_app_retrieve_update_destroy'),
    path('<uuid:app_pk>/users/', user_views.ClientUserListCreateView.as_view(), name='client_user_list_create'),
    path('<uuid:app_pk>/users/<uuid:user_pk>/', user_views.ClientUserRetrieveUpdateDestroyView.as_view(), name='client_user_retrieve_update_destroy'),

    # For Owner to manage Subscriptions
    path('<uuid:app_pk>/subscriptions/', subscription_views.SubscriptionListCreateView.as_view(), name='subscription_list_create'),
    path('payment/success/', subscription_views.handle_payment_success, name="payment_success"),
    path('<uuid:app_pk>/subscriptions/<uuid:subscription_pk>/', subscription_views.SubscriptionRetrieveUpdateDestroyView.as_view(), name='subscription_retrieve_update_destroy'),

    # For Client User to register, login, update, reset password, and verify email
    path('<uuid:app_pk>/users/register/', client_user_views.ClientUserRegisterView.as_view(), name='client_user_register'),
    path('<uuid:app_pk>/users/login/', client_user_views.ClientUserLoginView.as_view(), name='client_user_login'),

    # Login in client user via Oauth (This is the endpoint that the client app will redirect to after the user logs in via Google)
    path('users/login/google/callback', client_user_views.ClientUserGoogleLoginView.as_view(), name='client_user_google_login'),

    path('<uuid:app_pk>/users/my-profile/', client_user_views.ClientUserMyProfileView.as_view(), name='client_user_my_profile'),
    path('<uuid:app_pk>/users/update/<uuid:user_pk>/', client_user_views.ClientUserUpdateView.as_view(), name='client_user_update'),
    path('<uuid:app_pk>/users/reset-password/<uuid:user_pk>/', client_user_views.ClientUserResetPasswordView.as_view(), name='client_user_reset_password'),
    path('<uuid:app_pk>/users/verify-email/<uuid:user_pk>/', client_user_views.ClientUserVerifyEmailView.as_view(), name='client_user_verify_email'),

]