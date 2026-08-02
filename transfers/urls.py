from django.urls import path

from . import views

app_name = "transfers"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("beneficiaires/", views.recipients, name="recipients"),
    path("beneficiaires/<int:pk>/supprimer/", views.delete_recipient, name="delete_recipient"),
    path("nouveau-transfert/", views.new_transfer, name="new_transfer"),
    path("<int:pk>/annuler/", views.cancel_transfer, name="cancel_transfer"),
]
