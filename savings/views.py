from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import SavingsEnrollmentForm, SavingsOperationForm
from .models import SavingsAccount, SavingsOperation


@login_required
def overview(request):
    account = SavingsAccount.objects.filter(user=request.user).first()

    if account is None:
        if request.method == "POST":
            form = SavingsEnrollmentForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect("savings:overview")
        else:
            form = SavingsEnrollmentForm()
        return render(request, "savings/overview.html", {"account": None, "form": form})

    return _render_account(request, account, SavingsOperationForm(account=account, request=request))


def _render_account(request, account, operation_form):
    operations = list(account.operations.select_related("confirmed_by").all())
    confirmed = [o for o in operations if o.status == SavingsOperation.Status.CONFIRMED]
    totals = {
        "deposits": sum(o.amount for o in confirmed if o.operation_type == SavingsOperation.Type.DEPOSIT),
        "withdrawals": sum(o.amount for o in confirmed if o.operation_type == SavingsOperation.Type.WITHDRAWAL),
    }
    context = {
        "account": account,
        "operations": operations,
        "operation_form": operation_form,
        "totals": totals,
    }
    return render(request, "savings/overview.html", context)


@login_required
@require_POST
def request_operation(request):
    account = SavingsAccount.objects.filter(
        user=request.user, status=SavingsAccount.Status.ACTIVE
    ).first()
    if account is None:
        return redirect("savings:overview")

    form = SavingsOperationForm(request.POST, account=account, request=request)
    if form.is_valid():
        SavingsOperation.objects.create(
            account=account,
            operation_type=form.cleaned_data["operation_type"],
            amount=form.cleaned_data["amount"],
            note=form.cleaned_data["note"],
        )
        messages.success(request, "Votre demande a été envoyée. Un conseiller la confirmera rapidement.")
        return redirect("savings:overview")

    return _render_account(request, account, form)
