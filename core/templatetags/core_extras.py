from decimal import ROUND_HALF_UP, Decimal

from django import template

register = template.Library()

_MONTHS_FR = [
    "janv.", "févr.", "mars", "avr.", "mai", "juin",
    "juil.", "août", "sept.", "oct.", "nov.", "déc.",
]


@register.filter
def format_amount(amount, currency=""):
    """Mirror Intl.NumberFormat('fr-FR', {maximumFractionDigits: 2}) + ' CURRENCY'."""
    value = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    value = value.normalize()
    if value == value.to_integral_value():
        int_part, decimals = f"{int(value):d}", ""
    else:
        sign = "-" if value < 0 else ""
        value = abs(value)
        int_part, _, decimals = f"{value:.2f}".partition(".")
        int_part = f"{sign}{int_part}"

    grouped = f"{int(int_part):,}".replace(",", " ")
    formatted = f"{grouped},{decimals}" if decimals else grouped
    return f"{formatted} {currency}".strip()


@register.filter
def format_date(value):
    """Mirror the fr-FR 'DD MMM YYYY' short date format."""
    if not value:
        return ""
    return f"{value.day:02d} {_MONTHS_FR[value.month - 1]} {value.year}"


@register.filter
def dict_get(mapping, key):
    return mapping.get(key, "")


@register.filter
def capital(country_code):
    """Capital-city photo metadata for an ISO country code (see core.data.CAPITALS)."""
    from core.data import CAPITALS

    return CAPITALS.get(str(country_code or "").upper(), {})


@register.filter
def country_code(country_name):
    """ISO code for a country stored by name (e.g. "Zambie" -> "zm"), or ""."""
    from core.data import COUNTRIES

    name = str(country_name or "").strip().lower()
    for country in COUNTRIES:
        if country["name"].lower() == name or country["code"].lower() == name:
            return country["code"].lower()
    return ""


@register.filter
def initials(full_name):
    """Up to two initials for an avatar ("Grace Mbuyi" -> "GM")."""
    parts = [p for p in str(full_name or "").split() if p]
    return "".join(p[0] for p in parts[:2]).upper() or "?"


@register.simple_tag
def admin_overview():
    """Headline numbers for the Django admin home page."""
    from django.contrib.auth import get_user_model

    from marketing.models import Agency, ContactMessage
    from savings.models import SavingsAccount, SavingsOperation
    from transfers.models import Transfer

    return {
        "clients": get_user_model().objects.filter(is_staff=False).count(),
        "transfers_open": Transfer.objects.filter(
            status__in=[Transfer.Status.PENDING, Transfer.Status.PROCESSING]
        ).count(),
        "savings_pending": SavingsAccount.objects.filter(status=SavingsAccount.Status.PENDING).count()
        + SavingsOperation.objects.filter(status=SavingsOperation.Status.PENDING).count(),
        "messages_new": ContactMessage.objects.filter(is_handled=False).count(),
        "agencies": Agency.objects.filter(is_active=True).count(),
    }


_ADMIN_APP_ICONS = {
    "accounts": "users",
    "auth": "shield-check",
    "blog": "newspaper",
    "marketing": "globe-2",
    "savings": "piggy-bank",
    "transfers": "send",
}


@register.filter
def admin_app_icon(app_label):
    return _ADMIN_APP_ICONS.get(app_label, "layout-dashboard")


@register.simple_tag
def day_greeting():
    """Greeting for the current local time (settings.TIME_ZONE):
    morning until noon, afternoon until 18:00, evening after that."""
    from django.utils import timezone

    hour = timezone.localtime().hour
    if 5 <= hour < 12:
        return {"text": "Bonjour", "icon": "sun", "period": "morning"}
    if 12 <= hour < 18:
        return {"text": "Bon après-midi", "icon": "sun", "period": "afternoon"}
    return {"text": "Bonsoir", "icon": "moon", "period": "evening"}


@register.simple_tag(takes_context=True)
def seo_jsonld(context):
    """Structured data for search engines (schema.org JSON-LD): who Blue Sky
    is, under which names, where, and its official profiles. Helps Google
    show the site first for brand searches like "Africa Blue Sky"."""
    import json

    from django.conf import settings
    from django.templatetags.static import static
    from django.utils.safestring import mark_safe

    from core.data import SITE

    base = settings.SITE_URL.rstrip("/")
    countries = context.get("COUNTRIES") or []
    names = ["Africa Blue Sky", "AfricaBlueSky", "Blue Sky", "Blue Sky Money Transfer", "Blue Sky Africa"]
    same_as = [u for k, u in SITE.get("social", {}).items() if k in ("facebook", "tiktok")]
    organization = {
        "@type": ["Organization", "FinancialService"],
        "@id": base + "/#organization",
        "name": "Africa Blue Sky",
        "alternateName": names[1:],
        "legalName": "Blue Sky Money Transfer",
        "url": base + "/",
        "logo": base + static("img/favicon-512.png"),
        "image": base + static("img/og-image.jpg"),
        "description": SITE.get("definition", ""),
        "email": SITE["primary_email"],
        "telephone": SITE["primary_phone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenue Kapenda & Mobutu, Quartier Makutano",
            "addressLocality": "Lubumbashi",
            "addressRegion": "Haut-Katanga",
            "addressCountry": "CD",
        },
        "areaServed": [
            {"@type": "Country", "name": getattr(c, "country_name", None) or (c.get("name") if isinstance(c, dict) else str(c))}
            for c in countries
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": SITE["primary_phone"],
            "email": SITE["primary_email"],
            "contactType": "customer service",
            "availableLanguage": ["French", "English", "Swahili"],
        },
        "sameAs": same_as,
    }
    website = {
        "@type": "WebSite",
        "@id": base + "/#website",
        "name": "Africa Blue Sky",
        "alternateName": names[1:],
        "url": base + "/",
        "inLanguage": ["fr", "en", "sw"],
        "publisher": {"@id": base + "/#organization"},
    }
    data = {"@context": "https://schema.org", "@graph": [organization, website]}
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\u003c")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')
