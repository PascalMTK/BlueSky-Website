from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from core.decorators import guest_only

from .forms import LoginForm, OTPVerificationForm, SignupForm
from .models import EmailVerification, User

PENDING_USER_SESSION_KEY = "pending_verification_user_id"
PENDING_NEXT_SESSION_KEY = "pending_verification_next"


def _send_otp(user):
    verification, code = EmailVerification.issue_for(user)
    send_mail(
        "Votre code de vérification Blue Sky",
        f"Bonjour {user.get_short_name()},\n\nVotre code Blue Sky est : {code}\n\nIl expire dans 10 minutes. Ne le partagez avec personne.",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return verification


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
            with transaction.atomic():
                user = User.objects.create_user(
                    email=form.cleaned_data["email"],
                    full_name=form.cleaned_data["full_name"],
                    password=form.cleaned_data["password"],
                    phone=form.cleaned_data["phone"],
                    country=form.cleaned_data["country"],
                    is_active=False,
                )
                _send_otp(user)
            request.session[PENDING_USER_SESSION_KEY] = user.pk
            request.session[PENDING_NEXT_SESSION_KEY] = next_url
            return redirect("accounts:verify_otp")
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
            inactive_user = User.objects.filter(email=form.cleaned_data["email"], is_active=False).first()
            if inactive_user and inactive_user.check_password(form.cleaned_data["password"]):
                request.session[PENDING_USER_SESSION_KEY] = inactive_user.pk
                request.session[PENDING_NEXT_SESSION_KEY] = next_url
                verification = EmailVerification.objects.filter(user=inactive_user).first()
                if not verification or verification.can_resend():
                    _send_otp(inactive_user)
                return redirect("accounts:verify_otp")
            form.add_error(None, "Adresse e-mail ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form, "next": next_url})


@guest_only
def verify_otp_view(request):
    user_id = request.session.get(PENDING_USER_SESSION_KEY)
    if not user_id:
        return redirect("accounts:signup")
    user = User.objects.filter(pk=user_id, is_active=False).first()
    if not user:
        request.session.pop(PENDING_USER_SESSION_KEY, None)
        return redirect("accounts:login")

    form = OTPVerificationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        verification = EmailVerification.objects.filter(user=user).first()
        if verification and verification.verify(form.cleaned_data["code"]):
            user.is_active = True
            user.save(update_fields=["is_active"])
            verification.delete()
            next_url = request.session.pop(PENDING_NEXT_SESSION_KEY, "")
            request.session.pop(PENDING_USER_SESSION_KEY, None)
            login(request, user)
            return redirect(_safe_next(request, next_url))
        if verification and timezone.now() >= verification.expires_at:
            form.add_error("code", "Ce code a expiré. Demandez un nouveau code.")
        else:
            form.add_error("code", "Code incorrect. Vérifiez puis réessayez.")

    return render(request, "accounts/verify_otp.html", {"form": form, "masked_email": _mask_email(user.email)})


@require_POST
@guest_only
def resend_otp_view(request):
    user_id = request.session.get(PENDING_USER_SESSION_KEY)
    user = User.objects.filter(pk=user_id, is_active=False).first() if user_id else None
    if not user:
        return redirect("accounts:signup")
    verification = EmailVerification.objects.filter(user=user).first()
    if verification and not verification.can_resend():
        return redirect("accounts:verify_otp")
    _send_otp(user)
    return redirect("accounts:verify_otp")


def _mask_email(email):
    local, domain = email.split("@", 1)
    visible = local[:2] if len(local) > 2 else local[:1]
    return f"{visible}{'*' * max(3, len(local) - len(visible))}@{domain}"


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
