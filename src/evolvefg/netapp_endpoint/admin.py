from django.contrib import admin

from views import User
from .models import *


@admin.register(MonitoringCallback)
class MonitoringCallbackAdmin (admin.ModelAdmin):
    list_display = ['id', 'externalId', 'monitoringType', 'ipv4Addr']


@admin.register(AnalyticsEventNotification)
class AnalyticsEventNotificationAdmin (admin.ModelAdmin):
    list_display = ['id', 'notifId']


@admin.register(Cell)
class CellAdmin (admin.ModelAdmin):
    list_display = ['id', 'cellId', 'latitude', 'longitude']

@admin.register(User)
class UserAdmin (admin.ModelAdmin):
    list_display = ['id', 'username', 'email']