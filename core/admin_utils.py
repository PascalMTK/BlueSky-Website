"""Small display helpers shared by the Django admin classes."""
from django.utils.html import format_html

# Status value -> colour of its badge in admin lists.
_TONES = {
    "PENDING": "amber",
    "PROCESSING": "blue",
    "COMPLETED": "green",
    "ACTIVE": "green",
    "CONFIRMED": "green",
    "CANCELLED": "red",
    "REJECTED": "red",
    "CLOSED": "grey",
}


def badge(label, tone="grey"):
    return format_html('<span class="bs-badge bs-badge-{}">{}</span>', tone, label)


def status_badge(value, label):
    return badge(label, _TONES.get(value, "grey"))


def yes_no_badge(value, yes="Oui", no="Non", yes_tone="green", no_tone="grey"):
    return badge(yes, yes_tone) if value else badge(no, no_tone)


def image_preview(image_field, height=140):
    if not image_field:
        return format_html('<span class="bs-muted">Aucune image</span>')
    return format_html(
        '<img src="{}" alt="" class="bs-thumb" style="height:{}px">', image_field.url, height
    )
