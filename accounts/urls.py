from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.login_view, name="login"),
    path("inscription/", views.signup_view, name="signup"),
    path("deconnexion/", views.logout_view, name="logout"),
]
