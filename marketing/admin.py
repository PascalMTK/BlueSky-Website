from django.contrib import admin

from .models import ContactMessage


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
