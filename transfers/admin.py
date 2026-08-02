from django.contrib import admin

from .models import Recipient, Transfer


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user", "country", "phone", "created_at"]
    search_fields = ["full_name", "user__email", "country"]
    list_filter = ["country"]


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = [
        "reference",
        "user",
        "recipient",
        "destination_country",
        "amount_sent",
        "currency_sent",
        "status",
        "created_at",
    ]
    list_filter = ["status", "currency_sent", "destination_country"]
    search_fields = ["reference", "user__email", "recipient__full_name"]
