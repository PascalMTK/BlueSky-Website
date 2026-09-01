from django.urls import path

from . import views

app_name = "marketing"

urlpatterns = [
    path("", views.home, name="home"),
    path("a-propos/", views.about, name="about"),
    path("equipe/", views.team, name="team"),
    path("impact/", views.impact, name="impact"),
    path("tarifs/", views.tariffs, name="tariffs"),
    path("informations-paiement/", views.payment_information, name="payment_information"),
    path("pays/", views.countries, name="countries"),
    path("contact/", views.contact, name="contact"),
]
