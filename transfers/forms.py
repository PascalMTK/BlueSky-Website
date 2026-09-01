from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

from core.data import CURRENCIES, SITE
from core.data import COUNTRIES
from core.forms import StyledFormMixin
from core.i18n import SOURCE_LANGUAGE, translate

from .models import Recipient, Transfer

COUNTRY_CHOICES = [("", "Sélectionnez un pays")] + [
    (c["name"], f"{c['flag']} {c['name']}") for c in COUNTRIES
]
CURRENCY_CHOICES = [(c, c) for c in CURRENCIES]
PAYMENT_METHOD_CHOICES = [("", "Sélectionnez un moyen de paiement")] + [
    (p, p) for p in SITE["payment_partners"]
]


def _country_choices(lang):
    return [("", translate("Sélectionnez un pays", lang))] + [
        (c["name"], f"{c['flag']} {translate(c['name'], lang)}") for c in COUNTRIES
    ]


class RecipientForm(StyledFormMixin, forms.ModelForm):
    full_name = forms.CharField(
        label="Nom complet",
        min_length=2,
        error_messages={
            "required": "Nom du bénéficiaire requis",
            "min_length": "Nom du bénéficiaire requis",
        },
    )
    country = forms.ChoiceField(
        label="Pays",
        choices=COUNTRY_CHOICES,
        error_messages={
            "required": "Sélectionnez un pays",
            "invalid_choice": "Sélectionnez un pays",
        },
    )
    phone = forms.CharField(label="Téléphone (optionnel)", required=False)
    relationship = forms.CharField(
        label="Relation (optionnel)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex : Sœur, ami…"}),
    )

    class Meta:
        model = Recipient
        fields = ["full_name", "country", "phone", "relationship"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        lang = getattr(request, "active_language", SOURCE_LANGUAGE) if request else SOURCE_LANGUAGE
        self.fields["country"].choices = _country_choices(lang)


class TransferForm(StyledFormMixin, forms.ModelForm):
    recipient = forms.ModelChoiceField(
        label="Bénéficiaire",
        queryset=Recipient.objects.none(),
        empty_label="Sélectionnez un bénéficiaire",
        error_messages={
            "required": "Sélectionnez un bénéficiaire",
            "invalid_choice": "Sélectionnez un bénéficiaire",
        },
    )
    amount_sent = forms.DecimalField(
        label="Montant",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), "Le montant doit être supérieur à 0")],
        error_messages={
            "required": "Le montant doit être supérieur à 0",
            "invalid": "Le montant doit être supérieur à 0",
        },
        widget=forms.NumberInput(attrs={"min": "1", "step": "0.01"}),
    )
    currency_sent = forms.ChoiceField(label="Devise", choices=CURRENCY_CHOICES, initial="USD")
    payment_method = forms.ChoiceField(
        label="Moyen de paiement",
        choices=PAYMENT_METHOD_CHOICES,
        error_messages={
            "required": "Sélectionnez un moyen de paiement",
            "invalid_choice": "Sélectionnez un moyen de paiement",
        },
    )
    note = forms.CharField(label="Note (optionnel)", required=False, widget=forms.Textarea)

    class Meta:
        model = Transfer
        fields = ["recipient", "amount_sent", "currency_sent", "payment_method", "note"]

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipient"].queryset = Recipient.objects.filter(user=user)
        self.fields["recipient"].label_from_instance = (
            lambda r: f"{r.full_name}, {r.country}"
        )
