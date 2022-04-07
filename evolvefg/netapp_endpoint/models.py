from django.db import models


MONITORING_TYPE = (
    ('LOCATION_REPORTING','LOCATION_REPORTING'),
    ('LOSS_OF_CONNECTIVITY','LOSS_OF_CONNECTIVITY')
)

ANALYTICS_EVENT = (
    ('UE_MOBILITY','UE_MOBILITY'),
    ('UE_COMM','UE_COMM'),
    ('ABNORMAL_BEHAVIOR','ABNORMAL_BEHAVIOR'),
    ('CONGESTION','CONGESTION'),
    ('NETWORK_PERFORMANCE','NETWORK_PERFORMANCE'),
    ('QOS_SUSTAINABILITY','QOS_SUSTAINABILITY'),
)


def get_default_locationinfo():
    return {"cellId": "AAAAA1002", "enodeBId": "AAAAA1"}


def get_analyEventNotifs():
    return [
    {
      "analyEvent": "ABNORMAL_BEHAVIOR",
      "expiry": "2021-11-26T09:21:04.481Z",
      "timeStamp": "2021-11-26T09:21:04.481Z",
      "abnormalInfos": [
        {
          "gpsis": [
            "string"
          ],
          "appId": "string",
          "excep": {
            "excepId": "SUSPICION_OF_DDOS_ATTACK",
            "excepLevel": 0,
            "excepTrend": "UP"
          },
          "ratio": 100,
          "confidence": 0,
          "addtMeasInfo": {
            "ddosAttack": {
              "ipv4Addrs": [
                "198.51.100.1"
              ]
            }
          }
        }
      ]
    }
  ]


class MonitoringCallback (models.Model):
    externalId = models.CharField(max_length=30, null=True, blank=True)
    locationInfo = models.JSONField(
        default=get_default_locationinfo(),
        null=True,
        blank=True
    )
    monitoringType = models.CharField(max_length=25, choices=MONITORING_TYPE)
    subscription = models.CharField(max_length=100)
    ipv4Addr = models.CharField(max_length=15, null=True, blank=True)


class AnalyticsEventNotification (models.Model):
    notifId = models.CharField(max_length=100)
    analyEventNotifs = models.JSONField(
        default=get_analyEventNotifs(),
    )


class Cell (models.Model):
    cellId = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
