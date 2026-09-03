from django import template
from django.utils.safestring import mark_safe

from core.i18n import SOURCE_LANGUAGE, TRANSLATIONS

register = template.Library()


def _lookup(request, text):
    lang = getattr(request, "active_language", SOURCE_LANGUAGE) if request else SOURCE_LANGUAGE
    if lang == SOURCE_LANGUAGE:
        return text
    return TRANSLATIONS.get(lang, {}).get(text, text)


@register.simple_tag(takes_context=True)
def t(context, text):
    """Translate a plain-text string: {% t "Nous contacter" %}"""
    return _lookup(context.get("request"), text)


class BlockTNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        rendered = self.nodelist.render(context).strip()
        translated = _lookup(context.get("request"), rendered)
        # The dictionary is developer-authored (never user input), so it's
        # safe to mark as HTML — this is what lets a translated string keep
        # an inline <span> highlight, <br>, etc.
        return mark_safe(translated)


@register.tag(name="blockt")
def do_blockt(parser, token):
    """Translate a chunk of text that contains inline HTML, e.g. a
    highlighted <span>:
        {% blockt %}Envoyez plus <span class="text-brand-gold">loin</span>.{% endblockt %}
    The exact rendered HTML between the tags is the dictionary lookup key.
    """
    nodelist = parser.parse(("endblockt",))
    parser.delete_first_token()
    return BlockTNode(nodelist)
