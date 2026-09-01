from django.shortcuts import render

from core.data import COUNTRIES

from .forms import ContactForm
from .models import ContactMessage

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
