from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", core_views.sitemap_xml, name="sitemap"),
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
