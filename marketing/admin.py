from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "country", "created_at"]
    search_fields = ["full_name", "email", "message"]
    readonly_fields = ["full_name", "email", "country", "message", "created_at"]
