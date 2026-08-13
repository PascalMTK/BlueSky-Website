from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
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
