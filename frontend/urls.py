from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('owners/', views.owners, name="owners"),
    path('owners/list', views.owners_list, name="owners_list"),
    path('deals/', views.deals, name="deals"),
    path('deals/create', views.deals_create, name="deals_create"),
    path('deals/list', views.deals_list, name="deals_list"),
]
