from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Transfer


@login_required
def overview(request):
    transfers = (
        Transfer.objects.filter(user=request.user)
        .select_related("recipient")
        .order_by("-created_at")[:8]
    )
    pending_count = sum(1 for t in transfers if t.status == Transfer.Status.PENDING)
    completed_count = sum(1 for t in transfers if t.status == Transfer.Status.COMPLETED)

    stats = [
        ("send", "Transferts envoyés", len(transfers)),
        ("clock", "En attente", pending_count),
        ("check-circle-2", "Terminés", completed_count),
    ]

    context = {
        "transfers": transfers,
        "stats": stats,
        "first_name": request.user.full_name.split(" ")[0],
    }
    return render(request, "transfers/overview.html", context)


@login_required
@require_POST
def cancel_transfer(request, pk):
    Transfer.objects.filter(
        pk=pk, user=request.user, status=Transfer.Status.PENDING
    ).update(status=Transfer.Status.CANCELLED)
    return redirect("transfers:overview")
