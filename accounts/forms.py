from django import forms

from core.data import COUNTRIES
from core.forms import StyledFormMixin
from core.i18n import SOURCE_LANGUAGE, translate

from .models import User

COUNTRY_CHOICES = [("", "Sélectionnez votre pays")] + [
    (c["name"], f"{c['flag']} {c['name']}") for c in COUNTRIES
]


def _country_choices(lang):
    return [("", translate("Sélectionnez votre pays", lang))] + [
        (c["name"], f"{c['flag']} {translate(c['name'], lang)}") for c in COUNTRIES
    ]


class SignupForm(StyledFormMixin, forms.Form):
    full_name = forms.CharField(
        label="Nom complet",
        min_length=2,
        error_messages={
            "required": "Entrez votre nom complet",
            "min_length": "Entrez votre nom complet",
        },
    )
    email = forms.EmailField(
        label="Adresse e-mail",
        error_messages={
            "required": "Adresse e-mail invalide",
            "invalid": "Adresse e-mail invalide",
        },
    )
    phone = forms.CharField(
        label="Téléphone",
        min_length=6,
        error_messages={
            "required": "Numéro de téléphone invalide",
            "min_length": "Numéro de téléphone invalide",
        },
    )
    country = forms.ChoiceField(
        label="Pays",
        choices=COUNTRY_CHOICES,
        error_messages={
            "required": "Sélectionnez votre pays",
            "invalid_choice": "Sélectionnez votre pays",
        },
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            "required": "Le mot de passe doit contenir au moins 8 caractères",
            "min_length": "Le mot de passe doit contenir au moins 8 caractères",
        },
    )

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        lang = getattr(request, "active_language", SOURCE_LANGUAGE) if request else SOURCE_LANGUAGE
        self.fields["country"].choices = _country_choices(lang)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            self.add_error(None, "Un compte existe déjà avec cette adresse e-mail.")
            raise forms.ValidationError("Adresse e-mail déjà utilisée")
        return email

    def clean_full_name(self):
        return self.cleaned_data["full_name"].strip()


class LoginForm(StyledFormMixin, forms.Form):
    email = forms.EmailField(
        label="Adresse e-mail",
        error_messages={
            "required": "Adresse e-mail ou mot de passe invalide.",
            "invalid": "Adresse e-mail ou mot de passe invalide.",
        },
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        error_messages={"required": "Adresse e-mail ou mot de passe invalide."},
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()
