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
