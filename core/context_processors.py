from django.urls import reverse

from core.data import COUNTRIES, SITE
from core.i18n import AVAILABLE_LANGUAGES

NAV_ROUTES = [
    ("marketing:home", "Accueil"),
    ("marketing:about", "À propos"),
    ("marketing:team", "Équipe"),
    ("marketing:impact", "Impact"),
    ("blog:post_list", "Actualités"),
    ("marketing:countries", "Nos pays"),
    ("marketing:contact", "Contact"),
]

DASHBOARD_NAV_ROUTES = [
    ("transfers:overview", "Vue d'ensemble", "layout-dashboard"),
    ("transfers:recipients", "Bénéficiaires", "users"),
    ("transfers:new_transfer", "Nouveau transfert", "send"),
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
    nav_items = [(reverse(name), label) for name, label in NAV_ROUTES]
    nav_items.insert(1, (f"{reverse('marketing:home')}#epargne", "Épargne"))
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
        "COUNTRIES": COUNTRIES,
        "nav_items": nav_items,
        "dashboard_nav_items": dashboard_nav_items,
        "staff_nav_items": staff_nav_items,
        "AVAILABLE_LANGUAGES": AVAILABLE_LANGUAGES,
        "active_language": getattr(request, "active_language", "fr"),
    }
