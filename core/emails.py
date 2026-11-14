"""Branded e-mails sent to users (verification code and notifications).

Every message is rendered from templates/emails/<name>.html (which extends
emails/base.html), with a plain-text version derived from it. Replies go to
the Blue Sky contact address.

Notifications (welcome, savings, contact) never break the page that triggers
them: failures are logged and ignored. The verification code is the
exception — callers need to know when it could not be sent.
"""
import logging
import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.data import SITE

logger = logging.getLogger(__name__)


def _plain_text(html):
    text = re.sub(r"<(br|/p|/h1|/h2|/tr|/li)[^>]*>", "\n", html, flags=re.I)
    text = strip_tags(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def site_url(path=""):
    return settings.SITE_URL.rstrip("/") + path


def send_branded_email(to, subject, template, context=None, fail_silently=True):
    """Send templates/emails/<template>.html to one address. Returns True if sent."""
    if not to:
        return False
    ctx = {"SITE": SITE, "site_url": site_url(), "subject": subject}
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
    return send_branded_email(
        user.email, f"{code} est votre code de vérification Blue Sky", "otp",
        {"name": user.get_short_name(), "code": code}, fail_silently=False,
    )


def send_welcome(user):
    return send_branded_email(
        user.email, "Bienvenue chez Blue Sky", "welcome",
        {"name": user.get_short_name(), "dashboard_url": site_url("/tableau-de-bord/")},
    )


def send_savings_request_received(account):
    return send_branded_email(
        account.user.email, "Votre demande de compte épargne est bien reçue", "savings_request",
        {"name": account.user.get_short_name(), "savings_url": site_url("/epargne/")},
    )


def send_savings_activated(account):
    return send_branded_email(
        account.user.email, "Votre compte épargne Blue Sky est actif", "savings_activated",
        {"name": account.user.get_short_name(), "account": account, "savings_url": site_url("/epargne/")},
    )


def send_savings_rejected(account):
    return send_branded_email(
        account.user.email, "Votre demande de compte épargne", "savings_rejected",
        {"name": account.user.get_short_name()},
    )


def send_operation_requested(operation):
    return send_branded_email(
        operation.account.user.email, f"Demande de {operation.get_operation_type_display().lower()} reçue", "operation_requested",
        {"name": operation.account.user.get_short_name(), "op": operation, "savings_url": site_url("/epargne/")},
    )


def send_operation_result(operation):
    confirmed = operation.status == operation.Status.CONFIRMED
    kind = operation.get_operation_type_display().lower()
    subject = f"Votre {kind} est confirmé" if confirmed else f"Votre {kind} n'a pas pu être validé"
    return send_branded_email(
        operation.account.user.email, subject, "operation_result",
        {"name": operation.account.user.get_short_name(), "op": operation, "confirmed": confirmed,
         "account": operation.account, "savings_url": site_url("/epargne/")},
    )


def send_contact_acknowledgement(message):
    return send_branded_email(
        message.email, "Nous avons bien reçu votre message", "contact_ack",
        {"name": (message.full_name or "").split(" ")[0], "msg": message},
    )
