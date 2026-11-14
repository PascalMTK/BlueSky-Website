from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.data import COUNTRIES
from savings.models import SavingsAccount

from .forms import RecipientForm, TransferForm
from .models import Recipient, Transfer

COUNTRY_FLAGS = {c["name"]: c["flag"] for c in COUNTRIES}


@login_required
def overview(request):
    user_transfers = Transfer.objects.filter(user=request.user)
    transfers = user_transfers.select_related("recipient").order_by("-created_at")[:8]

    # Counts come from the whole history, not just the 8 rows shown below.
    by_status = dict(
        user_transfers.order_by().values_list("status").annotate(n=Count("id"))
    )
    total_count = sum(by_status.values())
    in_progress = by_status.get(Transfer.Status.PENDING, 0) + by_status.get(Transfer.Status.PROCESSING, 0)
    completed_count = by_status.get(Transfer.Status.COMPLETED, 0)

    # Money actually delivered, per currency (largest first).
    sent_totals = list(
        user_transfers.filter(status=Transfer.Status.COMPLETED)
        .order_by()
        .values("currency_sent")
        .annotate(total=Sum("amount_sent"))
        .order_by("-total")
    )

    recipients_qs = Recipient.objects.filter(user=request.user).order_by("-created_at")
    recipient_count = recipients_qs.count()

    stats = [
        ("send", "Transferts envoyés", total_count, "brand"),
        ("clock", "En cours de traitement", in_progress, "amber"),
        ("check-circle-2", "Transferts terminés", completed_count, "emerald"),
        ("users", "Bénéficiaires", recipient_count, "sky"),
    ]

    context = {
        "transfers": transfers,
        "recipient_count": recipient_count,
        "recent_recipients": recipients_qs[:4],
        "stats": stats,
        "sent_totals": sent_totals[:2],
        "success_rate": round(completed_count * 100 / total_count) if total_count else None,
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
            transfer.save()
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
