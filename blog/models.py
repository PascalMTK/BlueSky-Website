from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="Adresse (slug)")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="Résumé")
    body = models.TextField(verbose_name="Contenu")
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True, verbose_name="Image de couverture")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Auteur",
    )
    is_published = models.BooleanField(default=False, verbose_name="Publié")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Publié le")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "publication"
        verbose_name_plural = "publications"
        indexes = [models.Index(fields=["is_published", "published_at"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:220] or "article"
            slug = base_slug
            i = 2
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{i}"[:220]
                i += 1
            self.slug = slug
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
