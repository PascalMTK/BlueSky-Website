from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from core.decorators import guest_only

from .forms import LoginForm, SignupForm
from .models import User


def _safe_next(request, next_url):
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}
    ):
        return next_url
    return "/tableau-de-bord/"


@guest_only
def signup_view(request):
    next_url = request.GET.get("next", "")
    if request.method == "POST":
        next_url = request.POST.get("next", next_url)
        form = SignupForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                full_name=form.cleaned_data["full_name"],
                password=form.cleaned_data["password"],
                phone=form.cleaned_data["phone"],
                country=form.cleaned_data["country"],
            )
            login(request, user)
            return redirect(_safe_next(request, next_url))
    else:
        form = SignupForm(request=request)
    return render(request, "accounts/signup.html", {"form": form, "next": next_url})


@guest_only
def login_view(request):
    next_url = request.GET.get("next", "")
    if request.method == "POST":
        next_url = request.POST.get("next", next_url)
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect(_safe_next(request, next_url))
            form.add_error(None, "Adresse e-mail ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form, "next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
