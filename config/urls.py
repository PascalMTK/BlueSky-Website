from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("admin/", admin.site.urls),
    path("tableau-de-bord/", include("transfers.urls")),
    path("epargne/", include("savings.urls")),
    path("actualites/", include("blog.urls")),
    path("gestion/", include("staffpanel.urls")),
    path("", include("accounts.urls")),
    path("", include("marketing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
