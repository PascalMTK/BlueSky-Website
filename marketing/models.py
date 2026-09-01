from django.db import models


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
