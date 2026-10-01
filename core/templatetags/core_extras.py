from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()

_MONTHS_FR = [
    "janv.", "févr.", "mars", "avr.", "mai", "juin",
    "juil.", "août", "sept.", "oct.", "nov.", "déc.",
]


@lru_cache(maxsize=64)
def _flag_url(code):
    path = f"img/flags/{code}.jpg"
    return static(path) if finders.find(path) else ""


@register.simple_tag
def flag_url(code):
    """Static URL of a country's flag photo, or "" when none exists (e.g. a
    country added from the Admin that has no image yet)."""
    return _flag_url(str(code or "").lower())


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
