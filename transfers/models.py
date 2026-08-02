import secrets

from django.conf import settings
from django.db import models


def generate_reference():
    return f"BS-{secrets.token_hex(4).upper()}"


class Recipient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipients"
    )
    full_name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=32, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user"])]
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


class Transfer(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        PROCESSING = "PROCESSING", "En cours"
        COMPLETED = "COMPLETED", "Terminé"
        CANCELLED = "CANCELLED", "Annulé"

    reference = models.CharField(max_length=20, unique=True, default=generate_reference)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transfers"
    )
    recipient = models.ForeignKey(
        Recipient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="transfers",
    )
    origin_country = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    amount_sent = models.DecimalField(max_digits=12, decimal_places=2)
    currency_sent = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user"])]
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference
