from rest_framework import status, views, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .serializers import *
from .models import *
import mariadb
import sys
import json
import requests
import socket
import binascii
import datetime
import configparser
from evolved5g.sdk import LocationSubscriber
from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi
from evolved5g.swagger_client.models import Token
import os
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .renderers import UserJSONRenderer
from evolved5g.sdk import LocationSubscriber, QosAwareness, ConnectionMonitor
from evolved5g.swagger_client import UsageThreshold, Configuration, ApiClient, LoginApi

config = configparser.ConfigParser()
config.read('db_template.properties')  # it has to be changed with "db_template.properties" when filled


def request_nef_token(nef_host, username, password):
    configuration = Configuration()
    configuration.host = nef_host
    api_client = ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", username, password, "", "", "")

    return token


def monitor_subscription(times, host, access_token, certificate_folder, capifhost, capifport, callback_server):
    expire_time = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    netapp_id = "myNetapp"
    location_subscriber = LocationSubscriber(host, access_token, certificate_folder, capifhost, capifport)
    external_id = "10001@domain.com"

    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=callback_server,
        maximum_number_of_reports=times,
        monitor_expire_time=expire_time
    )
    monitoring_response = subscription.to_dict()

    return monitoring_response


def get_host_of_the_nef_emulator() -> str:
    nef_address = os.environ['NEF_ADDRESS']
    return "http://{}".format(nef_address)


def get_host_of_the_callback_server() -> str:
    callback_address = os.environ['CALLBACK_ADDRESS']
    return "http://{}".format(callback_address)


def get_vapp_server() -> str:
    vapp_address = os.environ['VAPP_ADDRESS']
    return "http://{}/ossimserver/asset/".format(vapp_address)


class MonitoringCallbackViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = MonitoringCallbackSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        return MonitoringCallback.objects.all()

    def create(self, request, *args, **kwargs):
        monitoringType = request.data["monitoringType"]
        if monitoringType == "LOSS_OF_CONNECTIVITY":
            pass
        elif monitoringType == "LOCATION_REPORTING":
            ipv4Addr = request.data["ipv4Addr"]
            externalId = request.data["externalId"]
            cellId = request.data["locationInfo"]["cellId"]

            cell = Cell.objects.get(cellId=cellId)
            lat = cell.latitude
            lon = cell.longitude

            vapp_host = get_vapp_server()
            payload = json.dumps({
                "external_id": externalId,
                "ipv4_addr": ipv4Addr,
                "latitude": lat,
                "longitude": lon
            })

            headers = {
                'Content-Type': 'application/json'
            }

            # Uncomment when testing with VApp
            requests.request('POST', vapp_host, headers=headers, data=payload)

        return super().create(request, *args, **kwargs)


class AnalyticsEventNotificationViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = AnalyticsEventNotificationSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        return AnalyticsEventNotification.objects.all()

    def create(self, request, *args, **kwargs):
        analyEventNotifs = request.data["analyEventNotifs"]
        for analyEventNotif in analyEventNotifs:
            if analyEventNotif["analyEvent"] == "UE_MOBILITY":
                if "ueMobilityInfos" not in analyEventNotif:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="'ueMobilityInfos' is missing")
            elif analyEventNotif["analyEvent"] == "UE_COMM":
                if "ueCommInfos" not in analyEventNotif:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="'ueCommInfos' is missing")
            elif analyEventNotif["analyEvent"] == "ABNORMAL_BEHAVIOR":
                if "abnormalInfos" not in analyEventNotif:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="'abnormalInfos' is missing")
            elif analyEventNotif["analyEvent"] == "CONGESTION":
                if "congestInfos" not in analyEventNotif:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="'congestInfos' is missing")
            elif analyEventNotif["analyEvent"] == "NETWORK_PERFORMANCE":
                if "nwPerfInfos" not in analyEventNotif:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="'nwPerfInfos' is missing")
            elif analyEventNotif["analyEvent"] == "QOS_SUSTAINABILITY":
                if "qosSustainInfos" not in analyEventNotif:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="'qosSustainInfos' is missing")

        return super().create(request, *args, **kwargs)


class CellViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = CellSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        return Cell.objects.all()


class CreateMonitoringSubscriptionView(APIView):

    def get(self, request, *args, **kwargs):

        times = self.kwargs.get('times')
        host = get_host_of_the_nef_emulator()
        nef_user = os.environ['NEF_USER']
        nef_pass = os.environ['NEF_PASSWORD']

        token = request_nef_token(host, nef_user, nef_pass)
        callback_host = get_host_of_the_callback_server() + "/netappserver/api/v1/monitoring/callback/"

        monitoring_response = monitor_subscription(int(times), host, token.access_token, os.environ['PATH_TO_CERTS'],
                                            os.environ['CAPIF_HOSTNAME'], os.environ['CAPIF_PORT_HTTPS'], callback_host)

        print(monitoring_response)

        if times == 1:
            cellId = monitoring_response['location_info']['cell_id']
            print(cellId)
            cell = Cell.objects.get(cellId=cellId)
            lat = cell.latitude
            lon = cell.longitude

            vapp_host = get_vapp_server()
            payload = json.dumps({
                "external_id": monitoring_response['external_id'],
                "ipv4_addr": monitoring_response["ipv4_addr"],
                "latitude": lat,
                "longitude": lon
            })

            headers = {
                'Content-Type': 'application/json'
            }

            # Uncomment when testing with VApp
            response = requests.request('POST', vapp_host, headers=headers, data=payload)
            message = json.loads(response.text)
            status_code = response.status_code
            # message = monitoring_response
            # status_code = status.HTTP_201_CREATED

        else:
            message = monitoring_response
            status_code = status.HTTP_201_CREATED

        return Response(message, status=status_code)


class CellsUpdateView(APIView):

    def get(self, request, *args, **kwargs):
        host = get_host_of_the_nef_emulator()
        nef_user = os.environ['NEF_USER']
        nef_pass = os.environ['NEF_PASSWORD']

        token = request_nef_token(host, nef_user, nef_pass)

        #    Call Monitoring API
        url = host + "/api/v1/Cells?skip=0&limit=100"

        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + token.access_token
        }

        response = requests.request('GET', url, headers=headers)
        parsed = json.loads(response.text)
        for cell in parsed:
            Cell.objects.update_or_create(cellId=cell['cell_id'], latitude=cell['latitude'], longitude=cell['longitude'])

        return Response(parsed, status=status.HTTP_201_CREATED)


# User View Set
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    print(Response(serializer.data))
    return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    # queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLogIn(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username
        })


class UserRegister(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        user = serializer.save()
        # user = User.objects.create(
        #         username=data['username'],
        #         email=data['email'],
        #         first_name=data['first_name'],
        #         last_name=data['last_name'],
        #         password=data['password'],
        #         password_confirm=data['password_confirm']
        #     )
        # user.set_password(data['password'])
        user.save()
        return Response({
            'user': user,
        })
        # return super().post(request, *args, **kwargs)
#username=data['username'], email=data['email'], password=data['password'], first_name=data['first_name'], last_name=['last_name']


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        # "token": Token.objects.create(user)[1]
        })


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        # print(authenticate(request=request, username=request.data["email"], password=request.data["password"]))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)