from rest_framework import serializers
from .models import ClientApp, ClientUser, ClientUserCustomField, Subscription, Payment, ApiPlan
from datetime import timedelta

class SubscriptionSerializer(serializers.ModelSerializer):
    # payment = PaymentSerializer(write_only = True)

    no_of_days = serializers.IntegerField(write_only=True, required=True, min_value=1) # Add validationclient
    amount = serializers.FloatField(write_only=True, required=False, default=0.0)
    client_app = serializers.PrimaryKeyRelatedField(read_only=True)
    plan = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'start_date': {'read_only': True},
            'end_date': {'read_only': True},
            'api_key': {'read_only': True},
            'api_key_expires': {'read_only': True},

        }


class ClientAppSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = ClientApp
        fields = '__all__'


class ClientUserCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUserCustomField
        fields = ['key', 'value']

class ClientUserSerializer(serializers.ModelSerializer):
    custom_fields = ClientUserCustomFieldSerializer(many=True, read_only=True)

    class Meta:
        model = ClientUser
        fields = ['id', 'email', 'username', 'name', 'avatar', 'is_active', 'role', 'login_type', 'client_app', 'custom_fields']
        extra_kwargs = {
            'client_app': {'read_only': True},
        }


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'




    # while creating i am passing, no_of_days as extra info which i'll use to calculate end_date



class ApiPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiPlan
        fields = '__all__'