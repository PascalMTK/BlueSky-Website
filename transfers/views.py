from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.data import COUNTRIES

from .forms import RecipientForm, TransferForm
from .models import Recipient, Transfer

COUNTRY_FLAGS = {c["name"]: c["flag"] for c in COUNTRIES}


@login_required
def overview(request):
    transfers = (
        Transfer.objects.filter(user=request.user)
        .select_related("recipient")
        .order_by("-created_at")[:8]
    )
    recipient_count = Recipient.objects.filter(user=request.user).count()
    pending_count = sum(1 for t in transfers if t.status == Transfer.Status.PENDING)
    completed_count = sum(1 for t in transfers if t.status == Transfer.Status.COMPLETED)

    stats = [
        ("send", "Transferts envoyés", len(transfers)),
        ("clock", "En attente", pending_count),
        ("check-circle-2", "Terminés", completed_count),
        ("users", "Bénéficiaires", recipient_count),
    ]

    context = {
        "transfers": transfers,
        "recipient_count": recipient_count,
        "stats": stats,
        "first_name": request.user.full_name.split(" ")[0],
    }
    return render(request, "transfers/overview.html", context)


@login_required
def recipients(request):
    if request.method == "POST":
        form = RecipientForm(request.POST)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.user = request.user
            recipient.save()
            return redirect("transfers:recipients")
    else:
        form = RecipientForm()

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
