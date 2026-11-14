from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.data import COUNTRIES
from core.i18n import translate
from savings.models import SavingsAccount

from .forms import RecipientForm, TransferForm
from .models import Recipient, Transfer

COUNTRY_FLAGS = {c["name"]: c["flag"] for c in COUNTRIES}


@login_required
def overview(request):
    user_transfers = Transfer.objects.filter(user=request.user)
    transfers = user_transfers.select_related("recipient").order_by("-created_at")[:8]

    # Transfers are made at an agency; the client space is a personal record
    # of them. Cancelled ones are left out of every count and total.
    kept = user_transfers.exclude(status=Transfer.Status.CANCELLED)
    total_count = kept.count()
    month_start = timezone.localtime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = kept.filter(created_at__gte=month_start).count()
    country_count = kept.order_by().values("destination_country").distinct().count()

    # Amount recorded, per currency (largest first).
    sent_totals = list(
        kept.order_by()
        .values("currency_sent")
        .annotate(total=Sum("amount_sent"))
        .order_by("-total")
    )

    recipients_qs = Recipient.objects.filter(user=request.user).order_by("-created_at")
    recipient_count = recipients_qs.count()

    stats = [
        ("send", "Transferts enregistrés", total_count, "brand"),
        ("clock", "Ce mois-ci", this_month, "amber"),
        ("globe-2", "Pays de destination", country_count, "emerald"),
        ("users", "Bénéficiaires", recipient_count, "sky"),
    ]

    context = {
        "transfers": transfers,
        "recipient_count": recipient_count,
        "recent_recipients": recipients_qs[:4],
        "stats": stats,
        "sent_totals": sent_totals[:2],
        "savings_account": SavingsAccount.objects.filter(user=request.user).first(),
        "first_name": request.user.full_name.split(" ")[0],
    }
    return render(request, "transfers/overview.html", context)


@login_required
def recipients(request):
    if request.method == "POST":
        form = RecipientForm(request.POST, request=request)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.user = request.user
            recipient.save()
            return redirect("transfers:recipients")
    else:
        form = RecipientForm(request=request)

    recipient_list = Recipient.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "form": form,
        "recipients": recipient_list,
        "country_flags": COUNTRY_FLAGS,
    }
    return render(request, "transfers/recipients.html", context)


@login_required
@require_POST
def delete_recipient(request, pk):
    Recipient.objects.filter(pk=pk, user=request.user).delete()
    return redirect("transfers:recipients")


@login_required
def new_transfer(request):
    has_recipients = Recipient.objects.filter(user=request.user).exists()
    if not has_recipients:
        return render(request, "transfers/new_transfer.html", {"has_recipients": False})

    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.origin_country = request.user.country or "RDC"
            transfer.destination_country = transfer.recipient.country
            # A personal record of a transfer already made at an agency: it is
            # saved as done and never enters the staff work queue.
            transfer.status = Transfer.Status.COMPLETED
            transfer.save()
            lang = getattr(request, "active_language", "fr")
            messages.success(request, translate("Transfert enregistré dans votre historique.", lang))
            return redirect("transfers:overview")
    else:
        form = TransferForm(user=request.user)

    return render(
        request, "transfers/new_transfer.html", {"has_recipients": True, "form": form}
    )


@login_required
@require_POST
def cancel_transfer(request, pk):
    Transfer.objects.filter(
        pk=pk, user=request.user, status=Transfer.Status.PENDING
    ).update(status=Transfer.Status.CANCELLED)
    return redirect("transfers:overview")


@login_required
@require_POST
def delete_transfer(request, pk):
    """Remove one of the client's own records. Transfers the team is still
    handling (pending or in progress) cannot be deleted, only cancelled."""
    deleted, _ = Transfer.objects.filter(
        pk=pk, user=request.user, status__in=[Transfer.Status.COMPLETED, Transfer.Status.CANCELLED]
    ).delete()
    if deleted:
        lang = getattr(request, "active_language", "fr")
        messages.success(request, translate("Transfert supprimé de votre historique.", lang))
    return redirect("transfers:overview")
