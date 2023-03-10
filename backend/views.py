import json
import logging

import hubspot
import requests
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from hubspot.crm.deals import ApiException as DealsApiException
from hubspot.crm.deals import SimplePublicObjectInput
from hubspot.crm.owners import ApiException as OwnersApiException
from hubspot.utils.oauth import get_auth_url

from backend.models import Credentials, HubSpotDealProperty, HubSpotToken
from backend.utils.helpers import create_or_update
from backend.utils.views import JSONResponseMixin

logger = logging.getLogger(__name__)


class HubSpotClientMixin:
    def _get_user_token(self, user):
        return get_object_or_404(HubSpotToken, user=user)

    def _get_client(self, request):
        # Starting November 30, 2022, API keys will be sunset as an authentication method.
        # Learn more about this change: https://developers.hubspot.com/changelog/upcoming-api-key-sunset
        # and how to migrate an API key integration: https://developers.hubspot.com/docs/api/migrate-an-api-key-integration-to-a-private-app
        # to use a private app instead.

        hubspot_token = self._get_user_token(request.user)
        return hubspot.Client.create(access_token=hubspot_token.access_token)


class HubSpotAuthRedirectView(RedirectView):
    is_permanent = True
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        return get_auth_url(
            client_id=Credentials.client_id,
            redirect_uri=Credentials.redirect_uri,
            scopes=Credentials.scopes,
        )


@method_decorator(csrf_exempt, name="dispatch")
class HubSpotRefreshTokenView(View):
    def post(self, request, *args, **kwargs):
        hubspot_token = get_object_or_404(HubSpotToken, user=request.user)
        try:
            response = requests.post(
                "https://api.hubapi.com/oauth/v1/token",
                data={
                    "grant_type": "refresh_token",
                    "client_id": Credentials.client_id,
                    "client_secret": Credentials.client_secret,
                    "refresh_token": hubspot_token.refresh_token,
                },
            )
            response.raise_for_status()
            data = response.json()
            create_or_update(
                HubSpotToken,
                request.user.id,
                dict(
                    access_token=data.get("access_token", ""),
                    refresh_token=data.get("refresh_token", ""),
                ),
            )
            return redirect("/")

        except requests.exceptions.HTTPError as err:
            logger.warn(
                f"Couldn't store obtain Token for User#{request.user.id} -> {err}"
            )
            return redirect("hubspot_oauth_authorize")


class HubSpotCallbackView(View, JSONResponseMixin):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code", "")
        try:
            response = requests.post(
                "https://api.hubapi.com/oauth/v1/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": Credentials.client_id,
                    "client_secret": Credentials.client_secret,
                    "redirect_uri": Credentials.redirect_uri,
                    "code": code,
                },
            )
            response.raise_for_status()
            data = response.json()
            create_or_update(
                HubSpotToken,
                request.user.id,
                dict(
                    access_token=data.get("access_token", ""),
                    refresh_token=data.get("refresh_token", ""),
                ),
            )
            return self.render_to_json_response({"message": "ok"})
        except requests.exceptions.HTTPError as e:
            logger.warn(
                f"Couldn't store obtain Token for User#{request.user.id} -> {e}"
            )
            return self.render_to_json_response(
                {"error": {"message": e.reason, "status": e.status}}
            )


class HubSpotOwnerView(View, HubSpotClientMixin, JSONResponseMixin):
    def _get_crm_owners(self, request, limit=100, archived=False):
        client = self._get_client(request)
        try:
            response = client.crm.owners.owners_api.get_page(
                limit=limit, archived=archived
            )
            response = response.to_dict()
        except OwnersApiException as e:
            logger.warning(
                f"Exception when calling owners_api->get_page: {e.reason} - {e.status}"
            )
            response = {"error": {"message": e.reason, "status": e.status}}

        return response

    def get(self, request):
        response = self._get_crm_owners(request, limit=100, archived=False)
        return self.render_to_json_response(response)


@method_decorator(csrf_exempt, name="dispatch")
class HubSpotDealView(View, HubSpotClientMixin, JSONResponseMixin):
    def _get_crm_deals(self, request, limit=10, archived=False):
        client = self._get_client(request)
        try:
            response = client.crm.deals.basic_api.get_page(
                limit=limit, archived=archived
            )
            response = response.to_dict()
        except DealsApiException as e:
            logger.warning(
                f"Exception when calling basic_api->get_page: {e.reason} - {e.status}"
            )
            response = {"error": {"message": e.reason, "status": e.status}}

        return response

    def _post_crm_deals(self, request, properties):
        client = self._get_client(request)
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            response = client.crm.deals.basic_api.create(
                simple_public_object_input=simple_public_object_input
            )
            response = response.to_dict()
        except DealsApiException as e:
            logger.warning("Exception when calling basic_api->create: %s\n" % e)
            response = {"error": {"message": e.reason, "status": e.status}}

        return response

    def get(self, request):
        response = self._get_crm_deals(request, limit=10, archived=False)
        return self.render_to_json_response(response)

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            properties: HubSpotDealProperty = data
        except json.JSONDecodeError:
            return self.render_to_json_response(
                {"error": {"message": "Invalid JSON", "status": 400}}
            )

        response = self._post_crm_deals(request, properties)
        return self.render_to_json_response(response)
