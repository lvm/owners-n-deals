from dataclasses import dataclass, field
from typing import List, TypedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from backend.utils.models import SingletonMeta

UserModel = get_user_model()


@dataclass(frozen=True)
class HubSpotCredentials(metaclass=SingletonMeta):
    client_id: str = field(default_factory=str)
    client_secret: str = field(default_factory=str, repr=False)
    redirect_uri: str = field(default_factory=str)
    scopes: List[str] = field(default_factory=list)


class HubSpotToken(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=500)
    access_token = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("HubSpot Token")
        verbose_name_plural = _("HubSpot Tokens")


class HubSpotDealProperty(TypedDict):
    amount: str
    closedate: str
    dealname: str
    dealstage: str
    hubspot_owner_id: str
    pipeline: str


Credentials = HubSpotCredentials(
    client_id=settings.HUBSPOT_CLIENT_ID,
    client_secret=settings.HUBSPOT_CLIENT_SECRET,
    redirect_uri=settings.HUBSPOT_REDIRECT_URI,
    scopes=settings.HUBSPOT_SCOPES,
)
