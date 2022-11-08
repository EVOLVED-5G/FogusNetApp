from imaplib import _Authenticator
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


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

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name','username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

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

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="username",
        write_only=True
    )
    password = serializers.CharField(
        label="password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = _Authenticator(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

# class RegisterSerializer(serializers.ModelSerializer):
#   email = serializers.EmailField(
#     required=True,
#     validators=[UniqueValidator(queryset=User.objects.all())]
#   )
#   password = serializers.CharField(
#     write_only=True, required=True, validators=[validate_password])
#   password_confirm = serializers.CharField(write_only=True, required=True)
  
#   class Meta:
#     model = User
#     fields = ('first_name','last_name', 'username', 'email', 'password', 'password_confirm')
#     extra_kwargs = {
#       'first_name': {'required': True},
#       'last_name': {'required': True}
#     }
#   def validate(self, attrs):
#     if attrs['password'] != attrs['password_confirm']:
#       raise serializers.ValidationError(
#         {"password": "Password fields didn't match."})
#     return attrs
#   def create(self, validated_data):
#     user = User.objects.create(
#       username=validated_data['username'],
#       email=validated_data['email'],
#       first_name=validated_data['first_name'],
#       last_name=validated_data['last_name']
#     )
#     user.set_password(validated_data['password'])
#     user.save()
#     return user
