from django import forms

from core.data import COUNTRIES
from core.forms import StyledFormMixin

from .models import ContactMessage

COUNTRY_CHOICES = (
    [("", "Sélectionnez votre pays")]
    + [(c["name"], f"{c['flag']} {c['name']}") for c in COUNTRIES]
    + [("Autre", "Autre pays")]
)


class ContactForm(StyledFormMixin, forms.ModelForm):
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
    country = forms.ChoiceField(
        label="Pays",
        required=False,
        choices=COUNTRY_CHOICES,
    )
    service = forms.ChoiceField(
        label="Sujet de votre demande",
        choices=ContactMessage.Service.choices,
        initial=ContactMessage.Service.TRANSFER,
    )
    message = forms.CharField(
        label="Votre message",
        min_length=10,
        widget=forms.Textarea,
        error_messages={
            "required": "Votre message est un peu court",
            "min_length": "Votre message est un peu court",
        },
    )

    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "country", "service", "message"]

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_full_name(self):
        return self.cleaned_data["full_name"].strip()
