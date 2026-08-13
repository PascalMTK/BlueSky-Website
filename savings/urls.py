from django.urls import path

from . import views

app_name = "savings"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("operation/", views.request_operation, name="request_operation"),
]
