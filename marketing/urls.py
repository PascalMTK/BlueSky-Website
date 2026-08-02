from django.urls import path

from . import views

app_name = "marketing"

urlpatterns = [
    path("", views.home, name="home"),
    path("a-propos/", views.about, name="about"),
    path("equipe/", views.team, name="team"),
    path("impact/", views.impact, name="impact"),
    path("pays/", views.countries, name="countries"),
    path("contact/", views.contact, name="contact"),
]
