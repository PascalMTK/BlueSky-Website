from django.contrib import admin

from .models import SavingsAccount, SavingsOperation


@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ["fiche_number", "user", "status", "balance", "opened_at", "created_at"]
    list_filter = ["status"]
    search_fields = ["fiche_number", "user__email", "user__full_name", "id_number"]


@admin.register(SavingsOperation)
class SavingsOperationAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "operation_type",
        "amount",
        "status",
        "requested_at",
        "confirmed_by",
    ]
    list_filter = ["operation_type", "status"]
    search_fields = ["account__fiche_number", "account__user__email"]
