from django import forms

from core.data import COUNTRIES
from core.forms import StyledFormMixin
from core.i18n import SOURCE_LANGUAGE, translate, translated_choices

from .models import ContactMessage

COUNTRY_CHOICES = (
    [("", "Sélectionnez votre pays")]
    + [(c["name"], f"{c['flag']} {c['name']}") for c in COUNTRIES]
    + [("Autre", "Autre pays")]
)


def _country_choices(lang):
    return (
        [("", translate("Sélectionnez votre pays", lang))]
        + [(c["name"], f"{c['flag']} {translate(c['name'], lang)}") for c in COUNTRIES]
        + [("Autre", translate("Autre pays", lang))]
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

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        lang = getattr(request, "active_language", SOURCE_LANGUAGE) if request else SOURCE_LANGUAGE
        self.fields["country"].choices = _country_choices(lang)
        self.fields["service"].choices = translated_choices(ContactMessage.Service.choices, lang)

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_full_name(self):
        return self.cleaned_data["full_name"].strip()
