from django.contrib import admin, messages
from django.utils.text import Truncator

from core.admin_utils import badge, yes_no_badge

from .models import Agency, ContactMessage, PaymentAccount, PaymentLocation, TariffBand, TariffPlan


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ["country_name", "address", "phone_numbers_summary", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    list_filter = ["is_active"]
    search_fields = ["country_name", "address", "phone_numbers"]
    readonly_fields = ["updated_at"]
    fieldsets = [
        ("Pays", {"fields": ("country_name", "code", "flag"), "description": "Le code pays sert à afficher le drapeau (par exemple CD, ZM, NA)."}),
        ("Coordonnées", {"fields": ("address", "phone_numbers", "note")}),
        ("Affichage", {"fields": ("is_active", "display_order", "updated_at"), "description": "Décochez « Visible sur le site » pour masquer l'agence sans la supprimer."}),
    ]

    @admin.display(description="Téléphones")
    def phone_numbers_summary(self, obj):
        return " · ".join(obj.phones) or "—"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "country", "service", "preview", "handled", "created_at"]
    list_filter = ["is_handled", "service", "country"]
    search_fields = ["full_name", "email", "message"]
    date_hierarchy = "created_at"
    list_per_page = 30
    actions = ["mark_handled", "mark_unhandled"]
    readonly_fields = ["full_name", "email", "country", "service", "message", "created_at"]

    def has_add_permission(self, request):
        # Messages arrive from the website contact form only.
        return False
    fieldsets = [
        ("Expéditeur", {"fields": ("full_name", "email", "country", "service", "created_at")}),
        ("Message", {"fields": ("message",)}),
        ("Suivi", {"fields": ("is_handled",), "description": "Cochez « Traité » une fois que la personne a reçu une réponse."}),
    ]

    @admin.display(description="Message")
    def preview(self, obj):
        return Truncator(obj.message).chars(70)

    @admin.display(description="Suivi", ordering="is_handled")
    def handled(self, obj):
        return yes_no_badge(obj.is_handled, yes="Traité", no="Nouveau", no_tone="amber")

    @admin.action(description="Marquer comme traités")
    def mark_handled(self, request, queryset):
        count = queryset.update(is_handled=True)
        self.message_user(request, f"{count} message(s) marqué(s) comme traité(s).", messages.SUCCESS)

    @admin.action(description="Marquer comme nouveaux")
    def mark_unhandled(self, request, queryset):
        count = queryset.update(is_handled=False)
        self.message_user(request, f"{count} message(s) remis en « nouveau ».", messages.SUCCESS)


class TariffBandInline(admin.TabularInline):
    model = TariffBand
    extra = 0
    fields = ["min_amount", "max_amount", "fee_type", "fee_value", "display_order"]
    ordering = ["display_order", "min_amount"]
    verbose_name = "tranche"
    verbose_name_plural = "Tranches de la grille (du plus petit au plus grand montant)"


@admin.register(TariffPlan)
class TariffPlanAdmin(admin.ModelAdmin):
    list_display = ["title", "type_label", "scope_label", "band_count", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    list_filter = ["tariff_type", "is_active"]
    search_fields = ["title", "scope_label", "slogan"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["updated_at"]
    inlines = [TariffBandInline]
    fieldsets = [
        ("Grille", {"fields": ("title", "tariff_type", "scope_label", "slogan")}),
        ("Affichage", {"fields": ("is_active", "display_order", "updated_at")}),
        ("Options avancées", {"classes": ("collapse",), "fields": ("slug",)}),
    ]

    @admin.display(description="Type", ordering="tariff_type")
    def type_label(self, obj):
        return badge(obj.get_tariff_type_display(), "blue" if obj.tariff_type == TariffPlan.Type.SEND else "green")

    @admin.display(description="Tranches")
    def band_count(self, obj):
        return obj.bands.count()


class PaymentAccountInline(admin.TabularInline):
    model = PaymentAccount
    extra = 0
    fields = ["payment_method", "phone_number", "account_holder", "instruction", "is_active", "display_order"]
    verbose_name = "compte"
    verbose_name_plural = "Comptes de paiement"


@admin.register(PaymentLocation)
class PaymentLocationAdmin(admin.ModelAdmin):
    list_display = ["country", "city", "account_count", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    search_fields = ["country", "city", "cash_address"]
    readonly_fields = ["updated_at"]
    inlines = [PaymentAccountInline]

    @admin.display(description="Comptes")
    def account_count(self, obj):
        return obj.accounts.count()
