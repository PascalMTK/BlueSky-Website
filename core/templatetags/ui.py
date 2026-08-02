from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def kicker(text, tone="gold"):
    tone_class = "text-brand-blue dark:text-brand-cyan" if tone == "blue" else "text-brand-gold"
    return mark_safe(
        f'<span class="editorial-label {tone_class}">{escape(text)}</span>'
    )
