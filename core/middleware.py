from core.i18n import AVAILABLE_LANGUAGES, SOURCE_LANGUAGE

LANG_COOKIE_NAME = "bluesky_lang"
LANG_COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year

_VALID_CODES = {lang["code"] for lang in AVAILABLE_LANGUAGES}


class LanguageMiddleware:
    """Picks the visitor's language from `?lang=xx` (persisted to a cookie
    for later requests that don't repeat the param), defaulting to French —
    the language the site is actually written in. Templates read
    `request.active_language` (via the `{% t %}` / `{% blockt %}` tags in
    core/templatetags/i18n_extra.py) to serve the right copy; see
    core/i18n.py for how the translation dictionaries work.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requested = request.GET.get("lang")
        lang = requested or request.COOKIES.get(LANG_COOKIE_NAME) or SOURCE_LANGUAGE
        if lang not in _VALID_CODES:
            lang = SOURCE_LANGUAGE
        request.active_language = lang

        response = self.get_response(request)

        if requested and requested in _VALID_CODES:
            response.set_cookie(LANG_COOKIE_NAME, lang, max_age=LANG_COOKIE_MAX_AGE)

        return response


class AdminCentreAccessMiddleware:
    """The admin centre (/admin/) is for administrators (superusers) only.

    Clients and team members who are signed in and open /admin/ are sent
    back to their own space with a short explanation, instead of Django's
    "not authorised" login loop. Visitors who are not signed in still see
    the admin login page; admin.site.has_permission (core/admin.py) is the
    actual gate.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.urls import reverse

        user = getattr(request, "user", None)
        admin_root = reverse("admin:index")
        if (
            request.path.startswith(admin_root)
            and user is not None
            and user.is_authenticated
            and not user.is_superuser
        ):
            from django.contrib import messages
            from django.shortcuts import redirect

            from core.decorators import home_url_for

            messages.info(request, "Le centre d'administration est réservé aux administrateurs.")
            return redirect(home_url_for(user))
        return self.get_response(request)
