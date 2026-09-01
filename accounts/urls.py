from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.login_view, name="login"),
    path("inscription/", views.signup_view, name="signup"),
    path("verification/", views.verify_otp_view, name="verify_otp"),
    path("verification/renvoyer/", views.resend_otp_view, name="resend_otp"),
    path("deconnexion/", views.logout_view, name="logout"),
    # Backwards-compatible links used by the previous version of the site.
    path(
        "comptes/connexion/",
        RedirectView.as_view(pattern_name="accounts:login", permanent=True),
        name="legacy_login",
    ),
    path(
        "comptes/inscription/",
        RedirectView.as_view(pattern_name="accounts:signup", permanent=True),
        name="legacy_signup",
    ),
]
