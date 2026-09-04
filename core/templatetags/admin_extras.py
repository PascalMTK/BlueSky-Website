from django import template

from accounts.models import User
from marketing.models import ContactMessage
from savings.models import SavingsAccount
from transfers.models import Transfer

register = template.Library()

# Maps an app's Django app_label to one of the Lucide icon keys defined in
# core/templatetags/icons.py, used on the admin dashboard app cards.
_APP_ICONS = {
    "accounts": "users",
    "auth": "shield-check",
    "blog": "newspaper",
    "marketing": "building-2",
    "savings": "piggy-bank",
    "transfers": "send",
    "staffpanel": "briefcase",
}


@register.simple_tag
def app_icon(app_label):
    return _APP_ICONS.get(app_label, "layout-dashboard")


@register.inclusion_tag("admin/includes/dashboard_stats.html")
def dashboard_stats():
    """Top-of-dashboard stat tiles. Each stat is safe to compute even on a
    fresh/empty database (counts just come back as 0)."""
    pending_transfers = Transfer.objects.filter(status=Transfer.Status.PENDING).count()
    unhandled_messages = ContactMessage.objects.filter(is_handled=False).count()
    stats = [
        {
            "label": "Utilisateurs",
            "value": User.objects.count(),
            "icon": "users",
            "url_name": "admin:accounts_user_changelist",
        },
        {
            "label": "Transferts en attente",
            "value": pending_transfers,
            "icon": "send",
            "url_name": "admin:transfers_transfer_changelist",
            "warn": pending_transfers > 0,
        },
        {
            "label": "Messages non traités",
            "value": unhandled_messages,
            "icon": "mail",
            "url_name": "admin:marketing_contactmessage_changelist",
            "warn": unhandled_messages > 0,
        },
        {
            "label": "Comptes épargne",
            "value": SavingsAccount.objects.count(),
            "icon": "piggy-bank",
            "url_name": "admin:savings_savingsaccount_changelist",
        },
    ]
    return {"stats": stats}
