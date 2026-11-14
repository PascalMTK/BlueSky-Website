from django.conf import settings
from django.urls import reverse

from core.data import COUNTRIES, SITE
from core.decorators import home_url_for
from core.i18n import AVAILABLE_LANGUAGES
from django.db.utils import OperationalError, ProgrammingError


def active_countries():
    """Return Admin-managed agencies, with static data as a pre-migration fallback."""
    try:
        from marketing.models import Agency

        return list(Agency.objects.filter(is_active=True))
    except (OperationalError, ProgrammingError):
        return COUNTRIES

NAV_ROUTES = [
    ("marketing:home", "Accueil", "house"),
    ("marketing:about", "À propos", "compass"),
    ("marketing:team", "Équipe", "users"),
    ("marketing:impact", "Impact", "heart-handshake"),
    ("marketing:tariffs", "Tarifs", "circle-dollar-sign"),
    ("blog:post_list", "Actualités", "newspaper"),
    ("marketing:countries", "Nos pays", "globe-2"),
    ("marketing:contact", "Contact", "mail"),
]

DASHBOARD_NAV_ROUTES = [
    ("transfers:overview", "Vue d'ensemble", "layout-dashboard"),
    ("transfers:recipients", "Bénéficiaires", "users"),
    ("transfers:new_transfer", "Enregistrer un transfert", "pencil"),
    ("marketing:payment_information", "Informations de paiement", "circle-dollar-sign"),
    ("savings:overview", "Épargne", "piggy-bank"),
]

STAFF_NAV_ROUTES = [
    ("staffpanel:home", "Tableau de bord", "layout-dashboard"),
    ("staffpanel:transfers", "Transferts", "send"),
    ("staffpanel:savings_accounts", "Comptes épargne", "piggy-bank"),
    ("staffpanel:messages", "Messages", "mail"),
    ("staffpanel:posts", "Publications", "newspaper"),
]


def site_data(request):
    countries = active_countries()
    nav_items = [(reverse(name), label, icon_name) for name, label, icon_name in NAV_ROUTES]
    nav_items.insert(1, (f"{reverse('marketing:home')}#epargne", "Épargne", "piggy-bank"))
    dashboard_nav_items = [
        (reverse(name), label, icon_name, True)
        for name, label, icon_name in DASHBOARD_NAV_ROUTES
    ]
    staff_nav_items = [
        (reverse(name), label, icon_name, True)
        for name, label, icon_name in STAFF_NAV_ROUTES
    ]
    return {
        "SITE": SITE,
        "COUNTRIES": countries,
        "nav_items": nav_items,
        "dashboard_nav_items": dashboard_nav_items,
        "staff_nav_items": staff_nav_items,
        "AVAILABLE_LANGUAGES": AVAILABLE_LANGUAGES,
        "ANALYTICS_GA_ID": getattr(settings, "ANALYTICS_GA_ID", ""),
        "active_language": getattr(request, "active_language", "fr"),
        # Where "Mon compte" leads: the management space for the team,
        # the client space for everyone else.
        "account_home_url": home_url_for(getattr(request, "user", None)),
    }
