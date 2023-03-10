from django.shortcuts import redirect, render
from django.urls import reverse

from backend.models import HubSpotToken


def context_data(request):
    if request.user.is_anonymous:
        query_result = []
        access_token = ""
        refresh_token = ""
    else:
        query_result = HubSpotToken.objects.filter(user=request.user)
        user_token = query_result.first()
        access_token = user_token.access_token
        refresh_token = user_token.refresh_token

    data = {
        "data": {
            "oauthAuthorize": reverse("hubspot_oauth_authorize"),
            "oauthRefreshToken": reverse("hubspot_refresh_token"),
            "ownersEndpoint": reverse('hubspot_owners'),
            "dealsEndpoint": reverse('hubspot_deals'),
            "userHasToken": "true" if len(query_result) > 0 else "false",
            "userToken": access_token,
            "userRefreshToken": refresh_token
        }
    }
    return data


# Home
def index(request):
    data = context_data(request)
    return render(request, 'frontend/index.html', data)

# Owners
def owners(request):
    return redirect('/owners/list')

def owners_list(request):
    data = context_data(request)
    return render(request, 'frontend/owners_list.html', data)

# Deals
def deals(request):
    return redirect('/deals/list')

def deals_create(request):
    data = context_data(request)
    return render(request, 'frontend/deals_create.html', data)

def deals_list(request):
    data = context_data(request)
    return render(request, 'frontend/deals_list.html', data)
