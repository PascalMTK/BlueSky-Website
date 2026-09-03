from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse


def guest_only(view_func):
    """Redirect already-authenticated users away from guest-only pages (login/signup)."""

    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("transfers:overview")
        return view_func(request, *args, **kwargs)

    return wrapped


def staff_required(view_func):
    """Gate staff-only views: anonymous users go to login, non-staff get a 403."""

    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped
