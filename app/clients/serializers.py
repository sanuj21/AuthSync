from rest_framework import serializers
from .models import ClientApp, ClientUser, ClientUserCustomField

class ClientAppSerializer(serializers.ModelSerializer):
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
