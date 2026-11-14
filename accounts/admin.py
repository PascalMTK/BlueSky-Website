from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from core.admin_utils import badge

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ["-created_at"]
    list_display = ["email", "full_name", "phone", "country", "role", "state", "created_at"]
    list_per_page = 30
    date_hierarchy = "created_at"
    list_filter = ["is_active", "is_staff", "is_superuser", "country"]
    search_fields = ["email", "full_name", "phone"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("full_name", "phone", "country")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ["created_at", "updated_at", "last_login"]

    @admin.display(description="Rôle", ordering="is_staff")
    def role(self, obj):
        if obj.is_superuser:
            return badge("Administrateur", "blue")
        if obj.is_staff:
            return badge("Équipe", "blue")
        return badge("Client", "grey")

    @admin.display(description="Compte", ordering="is_active")
    def state(self, obj):
        return badge("Actif", "green") if obj.is_active else badge("Désactivé", "red")
