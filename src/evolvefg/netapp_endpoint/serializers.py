from models import User
from rest_framework import serializers
from .models import *


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userId', 'username', 'email', 'password']

