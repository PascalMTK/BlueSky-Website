from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from core.admin_utils import badge

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ["-created_at"]
    list_display = ["email", "full_name", "phone", "country", "role", "state", "created_at"]
    list_per_page = 30
    date_hierarchy = "created_at"
    list_filter = ["is_staff", "is_superuser", "is_active", "country"]
    search_fields = ["email", "full_name", "phone"]
    # Access is decided by three switches only (no groups or per-user
    # permissions): client, team member (/gestion/), administrator (/admin/).
    filter_horizontal = ()
    fieldsets = (
        ("Compte", {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("full_name", "phone", "country")}),
        ("Accès", {
            "fields": ("is_active", "is_staff", "is_superuser"),
            "description": "Client : aucune case cochée. Membre de l'équipe : accès à l'espace gestion. "
                           "Administrateur : accès à l'espace gestion et au centre d'administration.",
        }),
        ("Dates", {"classes": ("collapse",), "fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        ("Nouveau compte", {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
        ("Accès", {
            "fields": ("is_staff", "is_superuser"),
            "description": "Laissez décoché pour un client.",
        }),
    )
    readonly_fields = ["created_at", "updated_at", "last_login"]

    _ACCESS_LABELS = {
        "is_active": ("Compte actif", "Décochez pour bloquer la connexion sans supprimer le compte."),
        "is_staff": ("Membre de l'équipe", "Accès à l'espace gestion (transferts, épargne, messages, publications)."),
        "is_superuser": ("Administrateur", "Accès complet, y compris le centre d'administration (tarifs, agences, comptes)."),
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if field is not None and db_field.name in self._ACCESS_LABELS:
            field.label, field.help_text = self._ACCESS_LABELS[db_field.name]
        return field

    def save_model(self, request, obj, form, change):
        # An administrator always has the team access too (Django's admin
        # login requires it).
        if obj.is_superuser:
            obj.is_staff = True
        super().save_model(request, obj, form, change)

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


# Groups are not used: access is set with the switches on each account.
admin.site.unregister(Group)
