from imaplib import _Authenticator
from rest_framework import serializers
from .models import *
# from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

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

# User serialezers
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username","first_name", "last_name","email", "password", "password_confirm"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "username", "email"]
    read_only_fields = ('username', )

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(
#         label="username",
#         write_only=True
#     )
    
#     password = serializers.CharField(
#         label="password",
#         trim_whitespace=False,
#         write_only=True
#     )

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#         if username and password:
#             user = authenticate( request=self.context.get('request'),
#                 username = username ,
#                 password=password)
#             if not user:
#                 # If we don't have a regular user, raise a ValidationError
#                 msg = 'Access denied: wrong username or password.'
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = 'Both "username" and "password" are required.'
#             raise serializers.ValidationError(msg, code='authorization')
#         attrs['user'] = user
#         return attrs

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['first_name', 'last_name','email', 'username','password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
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
