from django.db import models
from django.core.exceptions import ValidationError


class Agency(models.Model):
    code = models.CharField("Code pays", max_length=2, unique=True)
    country_name = models.CharField("Pays", max_length=100)
    flag = models.CharField("Drapeau", max_length=10, blank=True)
    address = models.TextField("Adresse de l'agence", blank=True)
    phone_numbers = models.TextField(
        "Numéros de téléphone",
        blank=True,
        help_text="Saisissez un numéro par ligne.",
    )
    note = models.TextField("Note", blank=True)
    is_active = models.BooleanField("Visible sur le site", default=True)
    display_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        ordering = ["display_order", "country_name"]
        verbose_name = "agence"
        verbose_name_plural = "agences"

    @property
    def name(self):
        return self.country_name

    @property
    def phones(self):
        return [number.strip() for number in self.phone_numbers.splitlines() if number.strip()]

    def __str__(self):
        return self.country_name


class ContactMessage(models.Model):
    class Service(models.TextChoices):
        TRANSFER = "transfert", "Transfert d'argent"
        SAVINGS = "epargne", "Épargne"
        OTHER = "autre", "Autre"

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    country = models.CharField(max_length=100, blank=True)
    service = models.CharField(
        max_length=20, choices=Service.choices, default=Service.TRANSFER
    )
    message = models.TextField()
    is_handled = models.BooleanField("Traité", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"


class TariffPlan(models.Model):
    class Type(models.TextChoices):
        SEND = "send", "Envoi"
        WITHDRAWAL = "withdrawal", "Retrait"

    slug = models.SlugField("Identifiant", unique=True)
    title = models.CharField("Titre", max_length=160)
    scope_label = models.CharField("Pays concernés", max_length=220)
    tariff_type = models.CharField("Type", max_length=20, choices=Type.choices)
    slogan = models.CharField("Slogan", max_length=220, blank=True)
    is_active = models.BooleanField("Visible sur le site", default=True)
    display_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "grille tarifaire"
        verbose_name_plural = "grilles tarifaires"

    def __str__(self):
        return self.title


class TariffBand(models.Model):
    class FeeType(models.TextChoices):
        FIXED = "fixed", "Montant fixe ($)"
        PERCENTAGE = "percentage", "Pourcentage (%)"

    plan = models.ForeignKey(
        TariffPlan,
        verbose_name="Grille tarifaire",
        related_name="bands",
        on_delete=models.CASCADE,
    )
    min_amount = models.DecimalField("Montant minimum ($)", max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(
        "Montant maximum ($)", max_digits=12, decimal_places=2, blank=True, null=True,
        help_text="Laissez vide pour une tranche sans limite.",
    )
    fee_type = models.CharField("Type de frais", max_length=16, choices=FeeType.choices)
    fee_value = models.DecimalField("Valeur des frais", max_digits=8, decimal_places=2)
    display_order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["display_order", "min_amount", "id"]
        verbose_name = "tranche tarifaire"
        verbose_name_plural = "tranches tarifaires"

    def clean(self):
        if self.max_amount is not None and self.max_amount < self.min_amount:
            raise ValidationError({"max_amount": "Le maximum doit être supérieur ou égal au minimum."})

    def __str__(self):
        maximum = self.max_amount if self.max_amount is not None else "illimité"
        return f"{self.plan}: {self.min_amount} à {maximum}"


class PaymentLocation(models.Model):
    country = models.CharField("Pays", max_length=100)
    city = models.CharField("Ville", max_length=100, blank=True)
    cash_address = models.TextField("Adresse de retrait cash", blank=True)
    slogan = models.CharField("Slogan", max_length=220, blank=True)
    is_active = models.BooleanField("Visible pour les clients", default=True)
    display_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        ordering = ["display_order", "country", "city"]
        verbose_name = "information de paiement"
        verbose_name_plural = "informations de paiement"

    def __str__(self):
        return f"{self.country}, {self.city}" if self.city else self.country


class PaymentAccount(models.Model):
    location = models.ForeignKey(
        PaymentLocation, related_name="accounts", on_delete=models.CASCADE,
        verbose_name="Pays / agence",
    )
    payment_method = models.CharField("Moyen de paiement", max_length=80)
    phone_number = models.CharField("Numéro", max_length=40)
    account_holder = models.CharField("Titulaire", max_length=140)
    instruction = models.CharField("Instruction particulière", max_length=220, blank=True)
    is_active = models.BooleanField("Visible", default=True)
    display_order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["display_order", "payment_method", "id"]
        verbose_name = "compte de paiement"
        verbose_name_plural = "comptes de paiement"

    def __str__(self):
        return f"{self.payment_method}, {self.phone_number}"
