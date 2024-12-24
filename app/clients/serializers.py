from rest_framework import serializers
from .models import ClientApp, ClientUser

class ClientAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientApp
        fields = '__all__'


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['id', 'email', 'username', 'name', 'avatar', 'is_active', 'role', 'login_type', 'client_app']
