from django.urls import reverse

from core.data import COUNTRIES, SITE

NAV_ROUTES = [
    ("marketing:home", "Accueil"),
    ("marketing:about", "À propos"),
    ("marketing:team", "Équipe"),
    ("marketing:impact", "Impact"),
    ("marketing:countries", "Nos pays"),
    ("marketing:contact", "Contact"),
]

DASHBOARD_NAV_ROUTES = [
    ("transfers:overview", "Vue d'ensemble", "layout-dashboard"),
    ("transfers:recipients", "Bénéficiaires", "users"),
    ("transfers:new_transfer", "Nouveau transfert", "send"),
]


def site_data(request):
    nav_items = [(reverse(name), label) for name, label in NAV_ROUTES]
    dashboard_nav_items = [
        (reverse(name), label, icon_name, True)
        for name, label, icon_name in DASHBOARD_NAV_ROUTES
    ]
    return {
        "SITE": SITE,
        "COUNTRIES": COUNTRIES,
        "nav_items": nav_items,
        "dashboard_nav_items": dashboard_nav_items,
    }
