from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from core.i18n import SOURCE_LANGUAGE, TRANSLATIONS

register = template.Library()


@register.simple_tag(takes_context=True)
def kicker(context, text, tone="gold"):
    """Section eyebrow: a short, quiet label above a heading.

    Plain sentence-case text in the brand colour, no decorative rule. The
    "gold" tone adapts to the background in CSS (deep amber on light sections,
    light gold on navy) so it always keeps enough contrast. motion.js reveals
    it word by word together with the heading below.
    """
    tone_class = "eyebrow-blue" if tone == "blue" else "eyebrow-gold"
    request = context.get("request")
    lang = getattr(request, "active_language", SOURCE_LANGUAGE) if request else SOURCE_LANGUAGE
    if lang != SOURCE_LANGUAGE:
        text = TRANSLATIONS.get(lang, {}).get(text, text)
    return mark_safe(f'<p class="eyebrow {tone_class}">{escape(text)}</p>')
