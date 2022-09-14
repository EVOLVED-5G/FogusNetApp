from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, mixins
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


config = configparser.ConfigParser()
config.read('db_template.properties')  # it has to be changed with "db_template.properties" when filled


def get_token() -> Token:
    configuration = swagger_client.Configuration()
    # The host of the 5G API (emulator)
    configuration.host = get_host_of_the_nef_emulator()
    api_client = swagger_client.ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    nef_user = config.get("nef", "nef_user")
    nef_pass = config.get("nef", "nef_pass")
    token = api.login_access_token_api_v1_login_access_token_post("", nef_user, nef_pass, "", "", "")
    return token


def get_host_of_the_nef_emulator() -> str:
    emulator = config.get("nef", "emulator")
    em_port = config.get("nef", "em_port")
    return "http://{}:{}".format(emulator, em_port)


def get_host_of_the_callback_server() -> str:
    cb_server = config.get("callback", "cb_server")
    cb_port = config.get("callback", "cb_port")
    return "http://{}:{}".format(cb_server, cb_port)


def get_vapp_server() -> str:
    vapp_server = config.get("vapp", "vapp_server")
    vapp_port = config.get("vapp", "vapp_port")
    return "http://{}:{}/ossimserver/asset/".format(vapp_server, vapp_port)


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
            # requests.request('POST', vapp_host, headers=headers, data=payload)

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
        expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
        netapp_id = "myNetapp"
        host = get_host_of_the_nef_emulator()
        token = get_token()
        location_subscriber = LocationSubscriber(host, token.access_token)
        external_id = "10001@domain.com"
        callback_host = get_host_of_the_callback_server()

        subscription = location_subscriber.create_subscription(
            netapp_id=netapp_id,
            external_id=external_id,
            notification_destination=callback_host + "/netappserver/api/v1/monitoring/callback/",
            maximum_number_of_reports=times,
            monitor_expire_time=expire_time
        )
        monitoring_response = subscription.to_dict()

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
            # response = requests.request('POST', vapp_host, headers=headers, data=payload)
            # message = json.loads(response.text)
            # status_code = response.status_code
            message = monitoring_response
            status_code = status.HTTP_201_CREATED

        else:
            message = subscription.to_dict()
            status_code = status.HTTP_201_CREATED

        return Response(message, status=status_code)


class CellsUpdateView(APIView):

    def get(self, request, *args, **kwargs):
        host = get_host_of_the_nef_emulator()
        token = get_token()

        #    Call Monitoring API
        url = host + "/api/v1/Cells?skip=0&limit=100"

        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + token.access_token
        }

        response = requests.request('GET', url, headers=headers)
        parsed = json.loads(response.text)
        for cell in parsed:
            Cell.objects.update_or_create(cellId=cell['cell_id'],latitude=cell['latitude'], longitude=cell['longitude'],)

        return Response(parsed, status=status.HTTP_201_CREATED)