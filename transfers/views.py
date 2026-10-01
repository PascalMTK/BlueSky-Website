from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Transfer


@login_required
def overview(request):
    user_transfers = Transfer.objects.filter(user=request.user)
    transfers = user_transfers.select_related("recipient").order_by("-created_at")[:8]
    counts = user_transfers.aggregate(
        total=Count("pk"),
        pending=Count("pk", filter=Q(status=Transfer.Status.PENDING)),
        completed=Count("pk", filter=Q(status=Transfer.Status.COMPLETED)),
    )

    stats = [
        ("send", "Transferts envoyés", counts["total"]),
        ("clock", "En attente", counts["pending"]),
        ("check-circle-2", "Terminés", counts["completed"]),
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
