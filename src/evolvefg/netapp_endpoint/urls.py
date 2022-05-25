from django.urls import path, include
from rest_framework import routers

from . import views
monitoring_callback_router = routers.SimpleRouter()
monitoring_callback_router.register(r'', views.MonitoringCallbackViewSet, basename='monitoringcallback')

analytics_callback_router = routers.SimpleRouter()
analytics_callback_router.register(r'', views.AnalyticsEventNotificationViewSet, basename='analyticscallback')


urlpatterns = [
    path(r'api/v1/monitoring/callback/', include(monitoring_callback_router.urls)),
    path(r'api/v1/analytics/callback/', include(analytics_callback_router.urls)),
    path(r'api/v1/monitoring/subscribe/<int:times>/', views.CreateMonitoringSubscriptionView.as_view(), name='monitoringsubscription'),
    path(r'api/v1/cells/update/', views.CellsUpdateView.as_view(), name='cellsupdate'),
]
