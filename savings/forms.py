from decimal import Decimal

from django import forms

from core.forms import StyledFormMixin

from .models import SavingsAccount, SavingsOperation


class SavingsEnrollmentForm(StyledFormMixin, forms.ModelForm):
    id_number = forms.CharField(
        label="N° CNI / Passeport",
        min_length=3,
        error_messages={
            "required": "Entrez votre numéro de CNI ou passeport",
            "min_length": "Entrez votre numéro de CNI ou passeport",
        },
    )
    address = forms.CharField(
        label="Adresse",
        min_length=3,
        error_messages={
            "required": "Entrez votre adresse",
            "min_length": "Entrez votre adresse",
        },
    )

    class Meta:
        model = SavingsAccount
        fields = ["id_number", "address"]


class SavingsOperationForm(StyledFormMixin, forms.Form):
    operation_type = forms.ChoiceField(
        label="Type d'opération", choices=SavingsOperation.Type.choices
    )
    amount = forms.DecimalField(
        label="Montant",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
        error_messages={
            "required": "Le montant doit être supérieur à 0",
            "invalid": "Le montant doit être supérieur à 0",
            "min_value": "Le montant doit être supérieur à 0",
        },
        widget=forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
    )
    note = forms.CharField(label="Observations (optionnel)", required=False, widget=forms.Textarea)

    def __init__(self, *args, account, **kwargs):
        self.account = account
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        operation_type = cleaned_data.get("operation_type")
        amount = cleaned_data.get("amount")
        if operation_type == SavingsOperation.Type.WITHDRAWAL and amount is not None:
            if amount > self.account.balance:
                self.add_error(
                    "amount",
                    f"Solde insuffisant : votre solde disponible est de {self.account.balance}.",
                )
        return cleaned_data
