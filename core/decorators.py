"""How the three spaces are routed and protected.

- Clients (``is_staff=False``) use the client space: /tableau-de-bord/,
  /epargne/, payment information.
- The team (``is_staff=True``) uses the management space: /gestion/.
- Superusers additionally get the Django admin: /admin/.

Everyone signs in on the same page; ``home_url_for`` decides where each
account lands afterwards.
"""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def home_url_for(user):
    """The space an account should land in after signing in."""
    if getattr(user, "is_authenticated", False) and user.is_staff:
        return reverse("staffpanel:home")
    return reverse("transfers:overview")


def guest_only(view_func):
    """Send already-signed-in users from login/signup to their own space."""

    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(home_url_for(request.user))
        return view_func(request, *args, **kwargs)

    return wrapped


def staff_required(view_func):
    """Gate the management space.

    Anonymous visitors are sent to the login page (and back here afterwards);
    signed-in clients are returned to their own space with an explanation
    instead of a bare "403 Forbidden".
    """

    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        if not request.user.is_staff:
            messages.info(request, "L'espace gestion est réservé à l'équipe Blue Sky.")
            return redirect("transfers:overview")
        return view_func(request, *args, **kwargs)

    return wrapped
