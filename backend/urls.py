from django.urls import path

from backend.views import (HubSpotAuthRedirectView, HubSpotCallbackView,
                           HubSpotDealView, HubSpotOwnerView,
                           HubSpotRefreshTokenView)

urlpatterns = [
    path(
        "hubspot/oauth/authorize",
        view=HubSpotAuthRedirectView.as_view(),
        name="hubspot_oauth_authorize",
    ),
    path(
        "hubspot/callback", view=HubSpotCallbackView.as_view(), name="hubspot_callback"
    ),
    path(
        "hubspot/refresh",
        view=HubSpotRefreshTokenView.as_view(),
        name="hubspot_refresh_token",
    ),
    path("hubspot/owners", view=HubSpotOwnerView.as_view(), name="hubspot_owners"),
    path("hubspot/deals", view=HubSpotDealView.as_view(), name="hubspot_deals"),
]
