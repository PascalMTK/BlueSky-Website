from django.contrib import admin, messages
from django.utils import timezone

from core.admin_utils import image_preview, yes_no_badge

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["cover_thumb", "title", "status", "author", "published_at", "updated_at"]
    list_display_links = ["cover_thumb", "title"]
    list_filter = ["is_published", "author"]
    search_fields = ["title", "excerpt", "body"]
    date_hierarchy = "created_at"
    list_per_page = 25
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["cover_preview", "created_at", "updated_at"]
    actions = ["publish", "unpublish"]
    save_on_top = False
    fieldsets = [
        ("Article", {
            "fields": ("title", "excerpt", "body"),
            "description": "Le titre et le résumé apparaissent dans la liste des actualités. Le contenu est le texte complet de l'article.",
        }),
        ("Image de couverture", {
            "fields": ("cover_preview", "cover_image"),
            "description": "Format paysage conseillé (par exemple 1600 × 900 pixels).",
        }),
        ("Publication", {
            "fields": ("is_published", "published_at", "author"),
            "description": "Cochez « Publié » pour afficher l'article sur le site. La date est remplie automatiquement si vous la laissez vide.",
        }),
        ("Options avancées", {
            "classes": ("collapse",),
            "fields": ("slug", "created_at", "updated_at"),
        }),
    ]

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.setdefault("author", request.user.pk)
        return initial

    @admin.display(description="", ordering="cover_image")
    def cover_thumb(self, obj):
        return image_preview(obj.cover_image, height=44)

    @admin.display(description="Aperçu")
    def cover_preview(self, obj):
        return image_preview(obj.cover_image if obj else None, height=160)

    @admin.display(description="Statut", ordering="is_published")
    def status(self, obj):
        return yes_no_badge(obj.is_published, yes="En ligne", no="Brouillon", no_tone="amber")

    @admin.action(description="Publier les publications sélectionnées")
    def publish(self, request, queryset):
        count = 0
        for post in queryset.filter(is_published=False):
            post.is_published = True
            post.published_at = post.published_at or timezone.now()
            post.save()
            count += 1
        self.message_user(request, f"{count} publication(s) mise(s) en ligne.", messages.SUCCESS)

    @admin.action(description="Repasser en brouillon")
    def unpublish(self, request, queryset):
        count = queryset.filter(is_published=True).update(is_published=False)
        self.message_user(request, f"{count} publication(s) retirée(s) du site.", messages.SUCCESS)
