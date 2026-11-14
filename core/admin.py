from django.contrib import admin

admin.site.site_header = "Administration Blue Sky"
admin.site.site_title = "Blue Sky Admin"
admin.site.index_title = "Vue d'ensemble"


def _administrators_only(request):
    """The admin centre is reserved to administrators (superusers); team
    members use the management space (/gestion/), clients their own space."""
    return request.user.is_active and request.user.is_superuser


admin.site.has_permission = _administrators_only
