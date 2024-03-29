from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate

class MonitoringCallbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonitoringCallback
        fields = ['id', 'externalId', 'locationInfo', 'monitoringType', 'subscription', 'ipv4Addr']

class AnalyticsEventNotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalyticsEventNotification
        fields = ['id', 'notifId', 'analyEventNotifs']

class CellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cell
        fields = ['id', 'cellId', 'latitude', 'longitude']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)
    password_confirm = serializers.CharField(write_only=True, min_length=8, required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'username','password',"password_confirm", 'token']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if not email:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        
        if not password:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        authenticated_user = authenticate(username=email, password=password)
        if not authenticated_user:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not authenticated_user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': authenticated_user.email,
            'username': authenticated_user.username,
            'token': authenticated_user.token
        }