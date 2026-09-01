from decimal import Decimal
from types import SimpleNamespace

from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.data import COUNTRIES

from .forms import ContactForm
from .models import ContactMessage, PaymentLocation, TariffPlan

FEATURES = [
    (
        "shield-check",
        "100% sécurisé",
        "Chaque transaction est protégée et suivie de bout en bout, sans mauvaise surprise.",
    ),
    (
        "zap",
        "Ultra rapide",
        "Vos bénéficiaires reçoivent leurs fonds en quelques minutes, pas en quelques jours.",
    ),
    (
        "globe-2",
        "Réseau régional",
        # The country count is interpolated in the template, outside this
        # translated string, so adding/removing a country in core/data.py
        # never desyncs a translation dictionary key (see core/i18n.py).
        "pays d'Afrique australe et de l'Est connectés à une seule plateforme.",
    ),
    (
        "headset",
        "Assistance humaine",
        "Une équipe joignable sur WhatsApp et par téléphone, dans chaque pays où nous opérons.",
    ),
]

SAVINGS_SEGMENTS = [
    (
        "graduation-cap",
        "Étudiants",
        "Mettez de côté pour vos frais académiques et vos projets d'avenir, à votre rythme.",
        "img/flags/portrait-male-student-with-books.jpg",
    ),
    (
        "house",
        "Familles",
        "Construisez un fonds commun pour les imprévus, les études des enfants ou un projet familial.",
        "img/flags/medium-shot-happy-african-people.jpg",
    ),
    (
        "briefcase",
        "Entreprises",
        "Épargnez pour votre fonds de roulement ou vos investissements, avec un suivi dédié.",
        "img/flags/tailors-working-with-quality-fabrics.jpg",
    ),
]

STEPS = [
    (
        "user-plus",
        "Créez votre compte",
        "Inscription en quelques minutes pour accéder à votre tableau de bord Blue Sky.",
    ),
    (
        "send",
        "Ajoutez un bénéficiaire",
        "Enregistrez les informations de la personne qui recevra les fonds.",
    ),
    (
        "check-circle-2",
        "Envoyez en toute confiance",
        "Choisissez le montant et le moyen de paiement, nous nous occupons du reste.",
    ),
]

def home(request):
    hero_stats = [
        (str(len(COUNTRIES)), "pays connectés"),
        ("7", "moyens de paiement"),
        ("100%", "suivi personnalisé"),
        ("1", "équipe à votre écoute"),
    ]
    context = {
        "features": FEATURES,
        "steps": STEPS,
        "hero_stats": hero_stats,
        "savings_segments": SAVINGS_SEGMENTS,
    }
    return render(request, "marketing/home.html", context)


def about(request):
    return render(request, "marketing/about.html")


VALUES = [
    (
        "handshake",
        "Proximité",
        "Des agents présents physiquement dans chaque pays, pas seulement une application.",
    ),
    (
        "ear",
        "Écoute",
        "Chaque client a une situation différente ; notre équipe prend le temps de comprendre.",
    ),
    (
        "rocket",
        "Réactivité",
        "Des réponses rapides sur WhatsApp et par téléphone, y compris en dehors des heures classiques.",
    ),
    (
        "heart-handshake",
        "Engagement",
        "Une équipe impliquée dans les communautés qu'elle sert, au-delà des transactions.",
    ),
]


def team(request):
    context = {"countries_count": len(COUNTRIES), "values": VALUES}
    return render(request, "marketing/team.html", context)


def impact(request):
    return render(request, "marketing/impact.html")


def countries(request):
    return render(request, "marketing/countries.html")


def tariffs(request):
    try:
        plans = list(TariffPlan.objects.filter(is_active=True).prefetch_related("bands"))
        for plan in plans:
            plan.display_bands = list(plan.bands.all())
        latest_update = max((plan.updated_at for plan in plans), default=None)
    except (OperationalError, ProgrammingError):
        # Keep the public page available during first deployment, before the
        # database migration has been applied. Once migrated, Admin data is
        # used automatically and this fallback is no longer reached.
        def band(minimum, maximum, fee_type, fee):
            return SimpleNamespace(
                min_amount=Decimal(str(minimum)),
                max_amount=Decimal(str(maximum)) if maximum is not None else None,
                fee_type=fee_type,
                fee_value=Decimal(str(fee)),
            )

        def plan(title, scope, tariff_type, slogan, bands):
            return SimpleNamespace(
                title=title,
                scope_label=scope,
                tariff_type=tariff_type,
                slogan=slogan,
                display_bands=[band(*values) for values in bands],
            )

        plans = [
            plan("Tarif spécial Tanzanie", "Transferts envoyés vers ou depuis la Tanzanie", "send", "Envoyez de l'argent en toute sécurité", [(2, 5, "fixed", 1), (6, 19, "fixed", 2), (20, 39, "fixed", 3), (40, 59, "fixed", 4), (60, 99, "fixed", 5), (100, 7500, "percentage", 4), (7501, None, "percentage", 3)]),
            plan("Tarif retrait quotidien", "Tarif standard du réseau Blue Sky", "withdrawal", "L'argent voyage en toute sécurité", [(1, 9, "fixed", 1), (10, 19, "fixed", 2), (20, 39, "fixed", 3), (40, 69, "fixed", 4), (70, 99, "fixed", 5), (100, 3000, "percentage", 5), (3001, 6000, "percentage", 4), (6001, None, "percentage", 3)]),
            plan("Tarif envoi quotidien", "Tarif standard du réseau Blue Sky", "send", "L'argent voyage en toute sécurité", [(1, 25, "fixed", 2), (26, 50, "fixed", 4), (51, 99, "fixed", 6), (100, 3000, "percentage", 5), (3001, None, "percentage", 3)]),
        ]
        latest_update = None
    return render(
        request,
        "marketing/tariffs.html",
        {"tariff_plans": plans, "latest_update": latest_update},
    )


@login_required
def payment_information(request):
    try:
        locations = list(PaymentLocation.objects.filter(is_active=True).prefetch_related("accounts"))
        for location in locations:
            location.visible_accounts = [account for account in location.accounts.all() if account.is_active]
    except (OperationalError, ProgrammingError):
        account_data = [
            ("Airtel Money", "+243 989 443 485", "Lord Kasisu", ""),
            ("Airtel Money", "+243 989 555 229", "Kasisu Josephine", ""),
            ("Airtel Money", "+243 989 474 804", "Lord Kasisu", ""),
            ("Airtel Money", "+243 997 266 023", "Elie Kayembe", "Effectuez uniquement un retrait. Aucun dépôt n'est autorisé."),
            ("M-Pesa", "+243 810 005 702", "Josephine Kasisu", ""),
            ("Orange Money", "+243 857 805 518", "Kayembe Elie", ""),
        ]
        locations = [SimpleNamespace(
            country="République démocratique du Congo", city="Lubumbashi",
            cash_address="Avenue Kapenda, coin Mobutu, en face de l'Hôtel Hypnose",
            slogan="L'argent voyage en toute sécurité", updated_at=None,
            visible_accounts=[SimpleNamespace(payment_method=method, phone_number=phone, account_holder=holder, instruction=instruction) for method, phone, holder, instruction in account_data],
        )]
    return render(request, "marketing/payment_information.html", {"locations": locations})


def contact(request):
    sent = False
    requested_service = request.GET.get("service")
    if requested_service not in dict(ContactMessage.Service.choices):
        requested_service = None

    if request.method == "POST":
        form = ContactForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            sent = True
            form = ContactForm(request=request)
    else:
        initial = {"service": requested_service} if requested_service else None
        form = ContactForm(initial=initial, request=request)
    return render(
        request,
        "marketing/contact.html",
        {"form": form, "sent": sent, "requested_service": requested_service},
    )
