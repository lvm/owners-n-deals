from django.contrib import admin

from backend.models import HubSpotToken


@admin.register(HubSpotToken)
class HubSpotTokenAdmin(admin.ModelAdmin):
    ...
