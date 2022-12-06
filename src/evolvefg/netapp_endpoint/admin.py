from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


@admin.register(MonitoringCallback)
class MonitoringCallbackAdmin (admin.ModelAdmin):
    list_display = ['id', 'externalId', 'monitoringType', 'ipv4Addr']


@admin.register(AnalyticsEventNotification)
class AnalyticsEventNotificationAdmin (admin.ModelAdmin):
    list_display = ['id', 'notifId']


@admin.register(Cell)
class CellAdmin (admin.ModelAdmin):
    list_display = ['id', 'cellId', 'latitude', 'longitude']

admin.site.register(User)