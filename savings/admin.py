from django.contrib import admin

from core.admin_utils import badge, status_badge

from .models import SavingsAccount, SavingsOperation

# Status changes that move money (activation, confirming a deposit or a
# withdrawal) are done from the staff space, which updates the balances.
# The admin shows them clearly but does not offer shortcuts around that.


@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ["fiche_number", "client", "status_label", "balance_usd", "opened_at", "created_at"]
    list_display_links = ["fiche_number", "client"]
    list_filter = ["status"]
    search_fields = ["fiche_number", "user__email", "user__full_name", "id_number"]
    list_select_related = ["user"]
    date_hierarchy = "created_at"
    list_per_page = 30
    autocomplete_fields = ["user"]

    @admin.display(description="Client", ordering="user__full_name")
    def client(self, obj):
        return obj.user.full_name or obj.user.email

    @admin.display(description="Statut", ordering="status")
    def status_label(self, obj):
        return status_badge(obj.status, obj.get_status_display())

    @admin.display(description="Solde", ordering="balance")
    def balance_usd(self, obj):
        return f"{obj.balance:,.2f} $".replace(",", " ")


@admin.register(SavingsOperation)
class SavingsOperationAdmin(admin.ModelAdmin):
    list_display = ["account", "type_label", "amount_usd", "status_label", "requested_at", "confirmed_by"]
    list_filter = ["operation_type", "status"]
    search_fields = ["account__fiche_number", "account__user__email", "account__user__full_name"]
    list_select_related = ["account__user", "confirmed_by"]
    date_hierarchy = "requested_at"
    list_per_page = 30

    @admin.display(description="Type", ordering="operation_type")
    def type_label(self, obj):
        tone = "green" if obj.operation_type == SavingsOperation.Type.DEPOSIT else "blue"
        return badge(obj.get_operation_type_display(), tone)

    @admin.display(description="Montant", ordering="amount")
    def amount_usd(self, obj):
        return f"{obj.amount:,.2f} $".replace(",", " ")

    @admin.display(description="Statut", ordering="status")
    def status_label(self, obj):
        return status_badge(obj.status, obj.get_status_display())
