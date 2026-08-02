from functools import wraps

from django.shortcuts import redirect


def guest_only(view_func):
    """Redirect already-authenticated users away from guest-only pages (login/signup)."""

    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("transfers:overview")
        return view_func(request, *args, **kwargs)

    return wrapped
