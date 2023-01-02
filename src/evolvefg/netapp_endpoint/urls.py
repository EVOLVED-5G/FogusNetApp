from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, UserDetailAPI
from . import views
import json

monitoring_callback_router = routers.SimpleRouter()
monitoring_callback_router.register(r'', views.MonitoringCallbackViewSet, basename='monitoringcallback')

analytics_callback_router = routers.SimpleRouter()
analytics_callback_router.register(r'', views.AnalyticsEventNotificationViewSet, basename='analyticscallback')

urlpatterns = [
    path(r'api/v1/monitoring/callback/', include(monitoring_callback_router.urls)),
    path(r'api/v1/analytics/callback/', include(analytics_callback_router.urls)),
    path(r'api/v1/monitoring/subscribe/<string>/', views.CreateMonitoringSubscriptionView.as_view(), name='monitoringsubscription'),
    path(r'api/v1/cells/update/', views.CellsUpdateView.as_view(), name='cellsupdate'),
    path('get-details/',UserDetailAPI.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('register/',views.RegistrationAPIView.as_view())
]