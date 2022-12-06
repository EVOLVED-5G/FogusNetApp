from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import jwt

from datetime import datetime, timedelta
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

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
    subscription = models.CharField(max_length=200)
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

class UserManager(BaseUserManager):
  # pass
  def create_user(self, first_name, last_name, email, username, password=None, password_confirm=None):
    if username is None:
      raise TypeError('Users must have a username.')

    if email is None:
      raise TypeError('Users must have an email address.')
    
    user = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name)
    # user = self.models(username=username, email=self.normalize_email(email), password=password, **other)
    user.set_password(password)
    user.save()

    return user

  def create_superuser(self, first_name, last_name, email, username, password):
    if password is None:
      raise TypeError('Superusers must have a password.')
    user = self.create_user(first_name=first_name, last_name=last_name,  email=email, username=username, password=password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user
    


class User(AbstractBaseUser, PermissionsMixin):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(db_index=True, unique=True)
  username = models.CharField(db_index=True, max_length=255, unique=True)
  password = models.CharField(max_length=100)
  password_confirm = models.CharField(max_length=100)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  objects = UserManager()

  def __str__(self):
    return {"email": self.email, "username": self.username}

  @property
  def token(self):
    return self._generate_jwt_token()

  def get_full_name(self):
    return self.username

  def get_short_name(self):
    return self.username
  
  def _generate_jwt_token(self):
    dt = datetime.now() + timedelta(days=60)
    token = jwt.encode({
        'id': self.pk,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')