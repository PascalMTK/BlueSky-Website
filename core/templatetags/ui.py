from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from core.i18n import SOURCE_LANGUAGE, TRANSLATIONS

register = template.Library()


@register.simple_tag(takes_context=True)
def kicker(context, text, tone="gold"):
    tone_class = "text-brand-blue dark:text-brand-cyan" if tone == "blue" else "text-brand-gold"
    request = context.get("request")
    lang = getattr(request, "active_language", SOURCE_LANGUAGE) if request else SOURCE_LANGUAGE
    if lang != SOURCE_LANGUAGE:
        text = TRANSLATIONS.get(lang, {}).get(text, text)
    return mark_safe(
        f'<span class="editorial-label {tone_class}">{escape(text)}</span>'
    )
