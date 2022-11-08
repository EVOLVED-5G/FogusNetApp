from django.contrib import admin
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