from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .serializers import *
from .models import *
from .renderers import *
from evolved5g.sdk import LocationSubscriber
from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi
from evolved5g.swagger_client.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from evolved5g.sdk import LocationSubscriber, QosAwareness, ConnectionMonitor
from evolved5g.swagger_client import UsageThreshold, Configuration, ApiClient, LoginApi
from rest_framework import status, views, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
import mariadb
import os
import sys
import json
import requests
import socket
import binascii
import datetime
import configparser
import os.path
from .renderers import UserJSONRenderer
from pathlib import Path

### Get token and environment variables ###
def request_nef_token(nef_host, username, password):
    configuration = Configuration()
    configuration.host = nef_host
    configuration.verify_ssl = False
    api_client = ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", username, password, "", "", "")
    return token

def get_host_of_the_nef_emulator() -> str:
    nef_address = os.environ['NEF_ADDRESS']
    return "https://{}".format(nef_address)

def get_host_of_the_callback_server() -> str:
    callback_address = os.environ['CALLBACK_ADDRESS']
    return "{}".format(callback_address)

def get_vapp_server() -> str:
    vapp_address = os.environ['VAPP_ADDRESS']
    return "https://{}/ossimserver/asset/".format(vapp_address)

def get_vapp_server_auth() -> str:
    vapp_address = os.environ['VAPP_ADDRESS']
    return "https://{}/ossimserver/auth-app/".format(vapp_address)

### For location reporting ###
def monitor_subscription(times, host, certificate_folder, capifhost, capifport, callback_server):
    expire_time = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    netapp_id = "myNetapp"
    location_subscriber = LocationSubscriber(host, certificate_folder, capifhost, capifport)
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

### For UE reachability ###
def connection_monitoring_ue_reachability(host, certificate_folder, capifhost, capifport, callback_server):
    expire_time = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    netapp_id = "myNetapp"
    monitoring_subscriber = ConnectionMonitor(host, certificate_folder, capifhost, capifport)
    external_id = "10001@domain.com"

    subscription = monitoring_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=callback_server,
        maximum_number_of_reports=2,
        monitor_expire_time=expire_time,
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED,
        wait_time_before_sending_notification_in_seconds=2
    )
    monitoring_response = subscription.to_dict()
    return monitoring_response

### For loss of connectivity ###
def connection_monitoring_loss_of_conn(host, certificate_folder, capifhost, capifport, callback_server):
    expire_time = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    netapp_id = "myNetapp"
    monitoring_subscriber = ConnectionMonitor(host, certificate_folder, capifhost, capifport)
    external_id = "10001@domain.com"
    
    subscription = monitoring_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=callback_server,
        maximum_number_of_reports=2,
        monitor_expire_time=expire_time,
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED ,
        wait_time_before_sending_notification_in_seconds=2
    )
    monitoring_response = subscription.to_dict()
    return monitoring_response

### Dynamic - For UE reachability and loss of connectivity ###
def connection_monitoring(times, MonitoringType_selected, host, certificate_folder, capifhost, capifport, callback_server):
    expire_time = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    netapp_id = "myNetapp"
    monitoring_subscriber = ConnectionMonitor(host, certificate_folder, capifhost, capifport)
    external_id = "10001@domain.com"
    
    subscription = monitoring_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=callback_server,
        maximum_number_of_reports=times,
        monitor_expire_time=expire_time,
        monitoring_type=MonitoringType_selected,
        wait_time_before_sending_notification_in_seconds=2
    )
    monitoring_response = subscription.to_dict()
    return monitoring_response

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
        headers = {
            'Content-Type': 'application/json'
        }
        monitoringType = request.data["monitoringType"]
        if monitoringType == "LOCATION_REPORTING":
            ipv4Addr = request.data["ipv4Addr"]
            externalId = request.data["externalId"]
            cellId = request.data["locationInfo"]["cellId"]
            cell = Cell.objects.get(cellId=cellId)
            lat = cell.latitude
            lon = cell.longitude
            payload = json.dumps({
                "externalId": externalId,
                "ipv4Addr": ipv4Addr,
                "latitude": lat,
                "longitude": lon
            })
            token_netapp = CreateMonitoringSubscriptionView.authentication_netapp(self)
            if token_netapp == "":
                token_netapp = CreateMonitoringSubscriptionView.authentication_netapp(self)
            with open('netapp.json', 'r') as openfile:
                # Reading from json file
                app_object = json.load(openfile)
                token_from_file = app_object['App information']['token']
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token'+token_from_file,
                }
            # Uncomment when testing with VApp
            vapp_host = get_vapp_server()
            # Add parameters for TLS
            response = requests.request('POST', vapp_host, headers=headers, data=payload, verify=False)
            status_code = response.status_code
        else:
            ipv4Addr = request.data["ipv4Addr"]
            externalId = request.data["externalId"]
        super().create(request,*args, **kwargs)
        return Response({"ack" : "TRUE"})

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
    ### Authenticate Network App ###
    def authentication_netapp(self):
        vapp_host = get_vapp_server_auth()
        app_address = os.environ['BACKEND_ADDRESS']
        app_name = "Fogus App"
        payload = json.dumps({
            "username":app_name,
            "app_address":app_address,
        })
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request('POST', vapp_host, headers=headers, data=payload, verify=False)
        message = json.loads(response.text)
        file_exists = os.path.exists('netapp.json')
        if file_exists is False:
            outfile = open("netapp.json", "x")
        if  "app with this app address already exists." in message['App information']['app_address'] :
             with open('netapp.json', 'r') as openfile:
                # Reading from json file
                app_object = json.load(openfile)
                token_netapp = app_object['App information']['token']
        elif  app_address in message['App information']['app_address']:
            token_netapp = message['App information']['token']
            with open("netapp.json", "w") as outfile:
                json.dump(message, outfile)
        else:
            token_netapp = ""
        return token_netapp


    def get(self, request, *args, **kwargs):
        answer = self.kwargs.get('string')
        answer_dict = answer.split("+")
        times = answer_dict[0]
        UE_selected = answer_dict[1]
        MonitoringType_selected = answer_dict[2]
        host = get_host_of_the_nef_emulator()
        nef_user = os.environ['NEF_USER']
        nef_pass = os.environ['NEF_PASSWORD']
        # token = request_nef_token(host, nef_user, nef_pass)
        # print("NEF TOKEN", token)
        callback_host = get_host_of_the_callback_server() + "/netappserver/api/v1/monitoring/callback/"
        if MonitoringType_selected == "LOCATION_REPORTING":
            monitoring_response = monitor_subscription(int(times), host, os.environ['PATH_TO_CERTS'],
                                            os.environ['CAPIF_HOSTNAME'], os.environ['CAPIF_PORT_HTTPS'], callback_host)
        elif MonitoringType_selected == "UE_REACHABILITY":
            # monitoring_type = ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED 
            # monitoring_response = connection_monitoring(int(times),monitoring_type, host, token.access_token, os.environ['PATH_TO_CERTS'],os.environ['CAPIF_HOSTNAME'], os.environ['CAPIF_PORT_HTTPS'], callback_host)
            monitoring_response = connection_monitoring_ue_reachability(host, os.environ['PATH_TO_CERTS'],
                                            os.environ['CAPIF_HOSTNAME'], os.environ['CAPIF_PORT_HTTPS'], callback_host)
        else:
            # monitoring_type = ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED 
            monitoring_response = connection_monitoring_loss_of_conn(host, os.environ['PATH_TO_CERTS'],
                                            os.environ['CAPIF_HOSTNAME'], os.environ['CAPIF_PORT_HTTPS'], callback_host)
        if int(times) == 1:
            cellId = monitoring_response['location_info']['cell_id']
            if cellId is None:
                print("None case")
                message = "Out of range"
                return Response(message)
            cell = Cell.objects.get(cellId=cellId)
            lat = cell.latitude
            lon = cell.longitude
            token_netapp = CreateMonitoringSubscriptionView.authentication_netapp(self)
            if token_netapp == "":
                token_netapp = CreateMonitoringSubscriptionView.authentication_netapp(self)
            vapp_host = get_vapp_server()
            payload = json.dumps({
                "externalId": monitoring_response['external_id'],
                "ipv4Addr": monitoring_response["ipv4_addr"],
                "latitude": lat,
                "longitude": lon
            })
            with open('netapp.json', 'r') as openfile:
                # Reading from json file
                app_object = json.load(openfile)
                token_from_file = app_object['App information']['token']
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token'+token_from_file,
                }
            # Uncomment when testing with VApp
            response = requests.request('POST', vapp_host, headers=headers, data=payload, verify= False)
            message = json.loads(response.text)
            status_code = response.status_code
        else:
            status_code = status.HTTP_201_CREATED
        message = monitoring_response
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

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)