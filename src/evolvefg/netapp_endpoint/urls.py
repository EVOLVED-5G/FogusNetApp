from django.urls import path, include
from macpath import basename
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views
from .views import users, register, login, AuthenticatedUser
from api import viewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

monitoring_callback_router = routers.SimpleRouter()
monitoring_callback_router.register(r'', views.MonitoringCallbackViewSet, basename='monitoringcallback')

analytics_callback_router = routers.SimpleRouter()
analytics_callback_router.register(r'', views.AnalyticsEventNotificationViewSet, basename='analyticscallback')

router = routers.SimpleRouter()
router.register('userapi', viewset.UserModelViewSet, basename = 'userapi')

urlpatterns = [
    path(r'api/v1/monitoring/callback/', include(monitoring_callback_router.urls)),
    path(r'api/v1/analytics/callback/', include(analytics_callback_router.urls)),
    path(r'api/v1/monitoring/subscribe/<int:times>/', views.CreateMonitoringSubscriptionView.as_view(), name='monitoringsubscription'),
    path(r'api/v1/cells/update/', views.CellsUpdateView.as_view(), name='cellsupdate'),
    path('', include(router.urls)),
    path('gettoken/', TokenObtainPairView.as_view(), name = 'gettoken'),
    path('refreshtoken/', TokenRefreshView.as_view(), name = 'refreshtoken'),
    path('verifytoken/', TokenVerifyView.as_view(), name = 'verifytoken')

    #path(r'api/users', users),
    #path(r'api/register', register),
    #path(r'api/user', AuthenticatedUser.as_view()),
]
