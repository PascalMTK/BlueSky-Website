from django.contrib import admin

from .models import Agency, ContactMessage, PaymentAccount, PaymentLocation, TariffBand, TariffPlan


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ["country_name", "address", "phone_numbers_summary", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    list_filter = ["is_active"]
    search_fields = ["country_name", "address", "phone_numbers"]
    readonly_fields = ["updated_at"]
    fieldsets = [
        ("Pays", {"fields": ("country_name", "code", "flag")}),
        ("Coordonnées", {"fields": ("address", "phone_numbers", "note")}),
        ("Affichage", {"fields": ("is_active", "display_order", "updated_at")}),
    ]

    @admin.display(description="Téléphones")
    def phone_numbers_summary(self, obj):
        return " · ".join(obj.phones) or "—"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "country", "service", "is_handled", "created_at"]
    list_filter = ["service", "is_handled"]
    search_fields = ["full_name", "email", "message"]
    readonly_fields = [
        "full_name",
        "email",
        "country",
        "service",
        "message",
        "created_at",
    ]


class TariffBandInline(admin.TabularInline):
    model = TariffBand
    extra = 0
    fields = ["min_amount", "max_amount", "fee_type", "fee_value", "display_order"]
    ordering = ["display_order", "min_amount"]


@admin.register(TariffPlan)
class TariffPlanAdmin(admin.ModelAdmin):
    list_display = ["title", "tariff_type", "scope_label", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    list_filter = ["tariff_type", "is_active"]
    search_fields = ["title", "scope_label", "slogan"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["updated_at"]
    inlines = [TariffBandInline]


class PaymentAccountInline(admin.TabularInline):
    model = PaymentAccount
    extra = 0
    fields = ["payment_method", "phone_number", "account_holder", "instruction", "is_active", "display_order"]


@admin.register(PaymentLocation)
class PaymentLocationAdmin(admin.ModelAdmin):
    list_display = ["country", "city", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    search_fields = ["country", "city", "cash_address"]
    readonly_fields = ["updated_at"]
    inlines = [PaymentAccountInline]
