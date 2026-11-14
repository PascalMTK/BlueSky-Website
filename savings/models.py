import secrets

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


def generate_fiche_number():
    return f"EP-{secrets.token_hex(3).upper()}"


class SavingsAccount(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente d'activation"
        ACTIVE = "ACTIVE", "Actif"
        REJECTED = "REJECTED", "Refusé"
        CLOSED = "CLOSED", "Clôturé"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="savings_account",
        verbose_name="Client",
    )
    fiche_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="N° de fiche")
    id_number = models.CharField("N° CNI / Passeport", max_length=50)
    address = models.CharField("Adresse", max_length=255)
    agent_name = models.CharField("Agent responsable", max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name="Statut")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Solde")
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name="Ouvert le")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Demandé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "compte épargne"
        verbose_name_plural = "comptes épargne"

    def __str__(self):
        return f"Fiche {self.fiche_number or '(non activée)'}, {self.user.full_name}"


class SavingsOperation(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Dépôt"
        WITHDRAWAL = "WITHDRAWAL", "Retrait"

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        REJECTED = "REJECTED", "Rejeté"

    account = models.ForeignKey(
        SavingsAccount, on_delete=models.CASCADE, related_name="operations",
        verbose_name="Compte",
    )
    operation_type = models.CharField(max_length=10, choices=Type.choices, verbose_name="Type d'opération")
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "Le montant doit être supérieur à 0")],
        verbose_name="Montant",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name="Statut")
    previous_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Solde précédent")
    new_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Nouveau solde")
    note = models.TextField("Observations", blank=True)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Confirmé par",
    )
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name="Demandé le")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Confirmé le")

    class Meta:
        ordering = ["-requested_at"]
        verbose_name = "opération d'épargne"
        verbose_name_plural = "opérations d'épargne"
        indexes = [models.Index(fields=["account"])]

    def __str__(self):
        return f"{self.get_operation_type_display()} de {self.amount}, {self.account}"
