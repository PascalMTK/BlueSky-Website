from django.contrib import admin, messages

from core.admin_utils import status_badge

from .models import Recipient, Transfer

# Same rules as the staff space (staffpanel.views.TRANSFER_TRANSITIONS).
ALLOWED_FROM = {
    Transfer.Status.PROCESSING: {Transfer.Status.PENDING},
    Transfer.Status.COMPLETED: {Transfer.Status.PROCESSING},
    Transfer.Status.CANCELLED: {Transfer.Status.PENDING, Transfer.Status.PROCESSING},
}


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user", "country", "phone", "relationship", "created_at"]
    search_fields = ["full_name", "user__email", "user__full_name", "country", "phone"]
    list_filter = ["country"]
    list_select_related = ["user"]
    autocomplete_fields = ["user"]
    list_per_page = 30


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ["reference", "client", "recipient", "route", "amount", "status_label", "created_at"]
    list_display_links = ["reference"]
    list_filter = ["status", "destination_country", "payment_method", "currency_sent"]
    search_fields = ["reference", "user__email", "user__full_name", "recipient__full_name"]
    list_select_related = ["user", "recipient"]
    date_hierarchy = "created_at"
    list_per_page = 30
    autocomplete_fields = ["user", "recipient"]
    readonly_fields = ["reference", "created_at", "updated_at"]
    actions = ["mark_processing", "mark_completed", "mark_cancelled"]
    fieldsets = [
        ("Transfert", {"fields": ("reference", "status")}),
        ("Client et bénéficiaire", {"fields": ("user", "recipient")}),
        ("Trajet et montant", {"fields": ("origin_country", "destination_country", "amount_sent", "currency_sent", "payment_method")}),
        ("Note interne", {"fields": ("note",)}),
        ("Dates", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    ]

    @admin.display(description="Client", ordering="user__full_name")
    def client(self, obj):
        return obj.user.full_name or obj.user.email

    @admin.display(description="Trajet", ordering="destination_country")
    def route(self, obj):
        return f"{obj.origin_country} → {obj.destination_country}"

    @admin.display(description="Montant", ordering="amount_sent")
    def amount(self, obj):
        return f"{obj.amount_sent:,.2f} {obj.currency_sent}".replace(",", " ")

    @admin.display(description="Statut", ordering="status")
    def status_label(self, obj):
        return status_badge(obj.status, obj.get_status_display())

    def _move(self, request, queryset, target):
        allowed = queryset.filter(status__in=ALLOWED_FROM[target])
        count = 0
        for transfer in allowed:
            transfer.status = target
            transfer.save(update_fields=["status", "updated_at"])
            count += 1
        skipped = queryset.count() - count
        if count:
            self.message_user(request, f"{count} transfert(s) passé(s) à « {Transfer.Status(target).label} ».", messages.SUCCESS)
        if skipped:
            self.message_user(request, f"{skipped} transfert(s) ignoré(s) : ce changement de statut n'est pas autorisé pour eux.", messages.WARNING)

    @admin.action(description="Prendre en charge (en attente → en cours)")
    def mark_processing(self, request, queryset):
        self._move(request, queryset, Transfer.Status.PROCESSING)

    @admin.action(description="Marquer terminé (en cours → terminé)")
    def mark_completed(self, request, queryset):
        self._move(request, queryset, Transfer.Status.COMPLETED)

    @admin.action(description="Annuler les transferts sélectionnés")
    def mark_cancelled(self, request, queryset):
        self._move(request, queryset, Transfer.Status.CANCELLED)
