from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page

# Public pages listed in the sitemap (private spaces and the admin are not).
PUBLIC_ROUTES = [
    ("marketing:home", "weekly", "1.0"),
    ("marketing:about", "monthly", "0.7"),
    ("marketing:team", "monthly", "0.6"),
    ("marketing:impact", "monthly", "0.6"),
    ("marketing:tariffs", "weekly", "0.9"),
    ("marketing:countries", "monthly", "0.8"),
    ("marketing:contact", "monthly", "0.8"),
    ("blog:post_list", "weekly", "0.7"),
    ("marketing:privacy", "yearly", "0.3"),
    ("marketing:terms", "yearly", "0.3"),
]


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /gestion/",
        "Disallow: /tableau-de-bord/",
        "Disallow: /epargne/",
        "Allow: /",
        "",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


@cache_page(60 * 60)
def sitemap_xml(request):
    from blog.models import Post

    urls = [
        (request.build_absolute_uri(reverse(name)), freq, prio, None)
        for name, freq, prio in PUBLIC_ROUTES
    ]
    for post in Post.objects.filter(is_published=True).only("slug", "updated_at"):
        try:
            url = request.build_absolute_uri(reverse("blog:post_detail", args=[post.slug]))
        except Exception:
            continue
        urls.append((url, "monthly", "0.6", post.updated_at.date().isoformat()))

    rows = []
    for loc, freq, prio, lastmod in urls:
        row = f"  <url><loc>{loc}</loc>"
        if lastmod:
            row += f"<lastmod>{lastmod}</lastmod>"
        row += f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        rows.append(row)
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    return HttpResponse(body, content_type="application/xml; charset=utf-8")
