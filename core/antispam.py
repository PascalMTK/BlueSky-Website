"""Light anti-spam for public forms.

- Honeypot: a "website" field hidden from people (CSS + aria-hidden); bots
  that fill every field reveal themselves.
- Rate limit: at most N submissions per visitor IP in a time window, kept in
  Django's cache.
"""
from django import forms
from django.core.cache import cache

HONEYPOT_FIELD = "website"


class HoneypotMixin(forms.Form):
    website = forms.CharField(
        required=False,
        label="Site web",
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )

    def is_spam(self):
        return bool((self.data.get(HONEYPOT_FIELD) or "").strip())


def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def rate_limited(request, scope, limit, window_seconds):
    """Count one attempt for this visitor; True once they are over the limit."""
    key = f"rl:{scope}:{client_ip(request)}"
    added = cache.add(key, 1, window_seconds)
    if added:
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, window_seconds)
        return False
    return count > limit
