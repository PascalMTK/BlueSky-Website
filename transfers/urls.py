from django.urls import path

from . import views

app_name = "transfers"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("<int:pk>/annuler/", views.cancel_transfer, name="cancel_transfer"),
]
