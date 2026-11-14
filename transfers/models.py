import secrets

from django.conf import settings
from django.db import models


def generate_reference():
    return f"BS-{secrets.token_hex(4).upper()}"


class Recipient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipients",
        verbose_name="Client",
    )
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    country = models.CharField(max_length=100, verbose_name="Pays")
    phone = models.CharField(max_length=32, blank=True, verbose_name="Téléphone")
    relationship = models.CharField(max_length=100, blank=True, verbose_name="Lien")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ajouté le")

    class Meta:
        indexes = [models.Index(fields=["user"])]
        ordering = ["-created_at"]
        verbose_name = "bénéficiaire"
        verbose_name_plural = "bénéficiaires"

    def __str__(self):
        return self.full_name


class Transfer(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        PROCESSING = "PROCESSING", "En cours"
        COMPLETED = "COMPLETED", "Terminé"
        CANCELLED = "CANCELLED", "Annulé"

    reference = models.CharField(max_length=20, unique=True, default=generate_reference, verbose_name="Référence")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transfers",
        verbose_name="Client",
    )
    recipient = models.ForeignKey(
        Recipient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="transfers",
        verbose_name="Bénéficiaire",
    )
    origin_country = models.CharField(max_length=100, verbose_name="Pays d'origine")
    destination_country = models.CharField(max_length=100, verbose_name="Pays de destination")
    amount_sent = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant envoyé")
    currency_sent = models.CharField(max_length=10, verbose_name="Devise")
    payment_method = models.CharField(max_length=50, verbose_name="Moyen de paiement")
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING,
        verbose_name="Statut",
    )
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Demandé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        indexes = [models.Index(fields=["user"])]
        ordering = ["-created_at"]
        verbose_name = "transfert"
        verbose_name_plural = "transferts"

    def __str__(self):
        return self.reference
