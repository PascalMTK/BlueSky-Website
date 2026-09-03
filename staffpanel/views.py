from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from blog.models import Post
from core.decorators import staff_required
from marketing.models import ContactMessage
from savings.models import SavingsAccount, SavingsOperation
from transfers.models import Transfer

from .forms import PostForm

# Legal next steps for a transfer, keyed by its current status — staff can
# only move a transfer forward or cancel it, never skip or rewind a step.
TRANSFER_TRANSITIONS = {
    Transfer.Status.PENDING: {Transfer.Status.PROCESSING, Transfer.Status.CANCELLED},
    Transfer.Status.PROCESSING: {Transfer.Status.COMPLETED, Transfer.Status.CANCELLED},
}


@staff_required
def home(request):
    context = {
        "pending_transfers": Transfer.objects.filter(status=Transfer.Status.PENDING).count(),
        "processing_transfers": Transfer.objects.filter(status=Transfer.Status.PROCESSING).count(),
        "pending_accounts": SavingsAccount.objects.filter(
            status=SavingsAccount.Status.PENDING
        ).count(),
        "pending_operations": SavingsOperation.objects.filter(
            status=SavingsOperation.Status.PENDING
        ).count(),
        "unhandled_messages": ContactMessage.objects.filter(is_handled=False).count(),
        "published_posts": Post.objects.filter(is_published=True).count(),
        "draft_posts": Post.objects.filter(is_published=False).count(),
    }
    return render(request, "staffpanel/home.html", context)


@staff_required
def transfers_list(request):
    status = request.GET.get("status", "")
    transfer_list = Transfer.objects.select_related("user", "recipient").all()
    if status:
        transfer_list = transfer_list.filter(status=status)
    context = {
        "transfer_list": transfer_list,
        "status": status,
        "status_choices": Transfer.Status.choices,
    }
    return render(request, "staffpanel/transfers.html", context)


@staff_required
@require_POST
def update_transfer_status(request, pk, status):
    transfer = get_object_or_404(Transfer, pk=pk)
    allowed = TRANSFER_TRANSITIONS.get(transfer.status, set())
    if status not in allowed:
        messages.error(request, "Ce changement de statut n'est pas autorisé.")
        return redirect("staffpanel:transfers")
    transfer.status = status
    transfer.save(update_fields=["status", "updated_at"])
    messages.success(request, f"Transfert {transfer.reference} mis à jour.")
    return redirect("staffpanel:transfers")


@staff_required
def savings_accounts(request):
    status = request.GET.get("status", "")
    accounts = SavingsAccount.objects.select_related("user").all()
    if status:
        accounts = accounts.filter(status=status)
    context = {
        "accounts": accounts,
        "status": status,
        "status_choices": SavingsAccount.Status.choices,
    }
    return render(request, "staffpanel/savings_accounts.html", context)


@staff_required
@require_POST
def activate_account(request, pk):
    account = get_object_or_404(SavingsAccount, pk=pk, status=SavingsAccount.Status.PENDING)
    account.status = SavingsAccount.Status.ACTIVE
    account.fiche_number = account.fiche_number or _generate_fiche_number()
    account.agent_name = request.user.full_name
    account.opened_at = timezone.now()
    account.save()
    messages.success(request, f"Compte de {account.user.full_name} activé.")
    return redirect("staffpanel:savings_account_detail", pk=account.pk)


@staff_required
@require_POST
def reject_account(request, pk):
    account = get_object_or_404(SavingsAccount, pk=pk, status=SavingsAccount.Status.PENDING)
    account.status = SavingsAccount.Status.REJECTED
    account.save()
    messages.success(request, f"Demande de {account.user.full_name} refusée.")
    return redirect("staffpanel:savings_accounts")


@staff_required
def savings_account_detail(request, pk):
    account = get_object_or_404(SavingsAccount.objects.select_related("user"), pk=pk)
    operations = account.operations.select_related("confirmed_by").all()
    context = {"account": account, "operations": operations}
    return render(request, "staffpanel/savings_account_detail.html", context)


@staff_required
@require_POST
def confirm_operation(request, pk):
    operation = get_object_or_404(
        SavingsOperation.objects.select_related("account"),
        pk=pk,
        status=SavingsOperation.Status.PENDING,
    )
    account = operation.account
    if operation.operation_type == SavingsOperation.Type.WITHDRAWAL and operation.amount > account.balance:
        messages.error(request, "Solde insuffisant pour confirmer ce retrait.")
        return redirect("staffpanel:savings_account_detail", pk=account.pk)

    operation.previous_balance = account.balance
    if operation.operation_type == SavingsOperation.Type.DEPOSIT:
        account.balance += operation.amount
    else:
        account.balance -= operation.amount
    operation.new_balance = account.balance
    operation.status = SavingsOperation.Status.CONFIRMED
    operation.confirmed_by = request.user
    operation.confirmed_at = timezone.now()
    account.save()
    operation.save()
    messages.success(request, "Opération confirmée.")
    return redirect("staffpanel:savings_account_detail", pk=account.pk)


@staff_required
@require_POST
def reject_operation(request, pk):
    operation = get_object_or_404(
        SavingsOperation.objects.select_related("account"),
        pk=pk,
        status=SavingsOperation.Status.PENDING,
    )
    operation.status = SavingsOperation.Status.REJECTED
    operation.confirmed_by = request.user
    operation.confirmed_at = timezone.now()
    operation.save()
    messages.success(request, "Opération rejetée.")
    return redirect("staffpanel:savings_account_detail", pk=operation.account.pk)


def _generate_fiche_number():
    from savings.models import generate_fiche_number

    number = generate_fiche_number()
    while SavingsAccount.objects.filter(fiche_number=number).exists():
        number = generate_fiche_number()
    return number


@staff_required
def posts(request):
    post_list = Post.objects.select_related("author").all()
    return render(request, "staffpanel/posts.html", {"posts": post_list})


@staff_required
def post_form(request, pk=None):
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            if not new_post.author_id:
                new_post.author = request.user
            new_post.save()
            messages.success(request, "Publication enregistrée.")
            return redirect("staffpanel:posts")
    else:
        form = PostForm(instance=post)
    return render(request, "staffpanel/post_form.html", {"form": form, "post": post})


@staff_required
@require_POST
def toggle_post_published(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.is_published = not post.is_published
    post.save()
    return redirect("staffpanel:posts")


@staff_required
@require_POST
def delete_post(request, pk):
    Post.objects.filter(pk=pk).delete()
    return redirect("staffpanel:posts")


@staff_required
def messages_list(request):
    handled = request.GET.get("handled", "")
    message_list = ContactMessage.objects.all()
    if handled == "1":
        message_list = message_list.filter(is_handled=True)
    elif handled == "0":
        message_list = message_list.filter(is_handled=False)
    context = {"message_list": message_list, "handled": handled}
    return render(request, "staffpanel/messages.html", context)


@staff_required
def message_detail(request, pk):
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    return render(request, "staffpanel/message_detail.html", {"contact_message": contact_message})


@staff_required
@require_POST
def toggle_message_handled(request, pk):
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    contact_message.is_handled = not contact_message.is_handled
    contact_message.save(update_fields=["is_handled"])
    return redirect("staffpanel:message_detail", pk=contact_message.pk)


@staff_required
@require_POST
def delete_message(request, pk):
    ContactMessage.objects.filter(pk=pk).delete()
    messages.success(request, "Message supprimé.")
    return redirect("staffpanel:messages")
