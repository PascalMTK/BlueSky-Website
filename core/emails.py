"""Branded e-mails sent to users (verification code and notifications).

Every message is rendered from templates/emails/<name>.html (which extends
emails/base.html) in the recipient's language — the language stored on their
account (User.language), or the visitor's current language for the contact
form. Templates use the same {% t %} translation tag as the site. A
plain-text version is derived from the HTML; replies go to the Blue Sky
contact address.

Notifications (welcome, savings, contact) never break the page that triggers
them: failures are logged and ignored. The verification code is the
exception — callers need to know when it could not be sent.
"""
import logging
import re
from types import SimpleNamespace

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.data import SITE
from core.i18n import AVAILABLE_LANGUAGES, SOURCE_LANGUAGE, translate

logger = logging.getLogger(__name__)
_CODES = {lang["code"] for lang in AVAILABLE_LANGUAGES}


def _lang(value):
    return value if value in _CODES else SOURCE_LANGUAGE


def user_lang(user):
    return _lang(getattr(user, "language", None))


def _plain_text(html):
    text = re.sub(r"<(br|/p|/h1|/h2|/tr|/li|/div)[^>]*>", "\n", html, flags=re.I)
    text = strip_tags(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def site_url(path=""):
    return settings.SITE_URL.rstrip("/") + path


def send_branded_email(to, subject, template, context=None, lang=SOURCE_LANGUAGE, fail_silently=True):
    """Send templates/emails/<template>.html to one address in `lang`.

    `subject` is the French text; it is translated like the template.
    Returns True if the message was sent.
    """
    if not to:
        return False
    lang = _lang(lang)
    subject = translate(subject, lang)
    ctx = {
        "SITE": SITE,
        "site_url": site_url(),
        "subject": subject,
        "lang": lang,
        # Neutral greeting (the site's "Bonjour" means "good morning").
        "greeting": {"fr": "Bonjour", "en": "Hello", "sw": "Habari"}[lang],
        # Lets the {% t %} tag in e-mail templates pick the recipient's language.
        "request": SimpleNamespace(active_language=lang),
    }
    ctx.update(context or {})
    html = render_to_string(f"emails/{template}.html", ctx)
    message = EmailMultiAlternatives(
        subject=subject,
        body=_plain_text(html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to],
        reply_to=[SITE["primary_email"]],
    )
    message.attach_alternative(html, "text/html")
    try:
        message.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("E-mail %r to %s could not be sent", template, to)
        if not fail_silently:
            raise
        return False


# --- Messages -------------------------------------------------------------

def send_verification_code(user, code):
    """Raises if the e-mail cannot be sent: the caller tells the visitor."""
    lang = user_lang(user)
    # The code leads the subject so it shows in the inbox list.
    subject = f"{code} · {translate('Votre code de vérification Blue Sky', lang)}"
    return send_branded_email(
        user.email, subject, "otp",
        {"name": user.get_short_name(), "code": code},
        lang=lang, fail_silently=False,
    )


def send_welcome(user):
    return send_branded_email(
        user.email, "Bienvenue chez Blue Sky", "welcome",
        {"name": user.get_short_name(), "dashboard_url": site_url("/tableau-de-bord/")},
        lang=user_lang(user),
    )


def send_savings_request_received(account):
    return send_branded_email(
        account.user.email, "Votre demande de compte épargne est bien reçue", "savings_request",
        {"name": account.user.get_short_name(), "savings_url": site_url("/epargne/")},
        lang=user_lang(account.user),
    )


def send_savings_activated(account):
    return send_branded_email(
        account.user.email, "Votre compte épargne Blue Sky est actif", "savings_activated",
        {"name": account.user.get_short_name(), "account": account, "savings_url": site_url("/epargne/")},
        lang=user_lang(account.user),
    )


def send_savings_rejected(account):
    return send_branded_email(
        account.user.email, "Votre demande de compte épargne n'a pas pu être validée", "savings_rejected",
        {"name": account.user.get_short_name()},
        lang=user_lang(account.user),
    )


def send_operation_requested(operation):
    return send_branded_email(
        operation.account.user.email, "Votre demande d'opération est bien reçue", "operation_requested",
        {"name": operation.account.user.get_short_name(), "op": operation,
         "op_label": operation.get_operation_type_display(), "savings_url": site_url("/epargne/")},
        lang=user_lang(operation.account.user),
    )


def send_operation_result(operation):
    confirmed = operation.status == operation.Status.CONFIRMED
    subject = "Votre opération est confirmée" if confirmed else "Votre opération n'a pas pu être validée"
    return send_branded_email(
        operation.account.user.email, subject, "operation_result",
        {"name": operation.account.user.get_short_name(), "op": operation, "confirmed": confirmed,
         "op_label": operation.get_operation_type_display(), "account": operation.account,
         "savings_url": site_url("/epargne/")},
        lang=user_lang(operation.account.user),
    )


def send_contact_acknowledgement(message, lang=SOURCE_LANGUAGE):
    return send_branded_email(
        message.email, "Nous avons bien reçu votre message", "contact_ack",
        {"name": (message.full_name or "").split(" ")[0], "msg": message},
        lang=lang,
    )
