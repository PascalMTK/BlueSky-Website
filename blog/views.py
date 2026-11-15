from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    posts = Post.objects.filter(is_published=True).select_related("author")
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    campaigns = [
        ("namibia.jpg", "La Namibie vous rapproche", "Envoyer et recevoir à travers l'Afrique."),
        ("confidence.jpg", "La confiance nous relie", "Vos transferts accompagnés par Blue Sky."),
        ("regional-transfers.jpg", "Un réseau sans frontières", "Des liens à travers nos pays partenaires."),
        ("from-uganda.jpg", "Depuis l'Ouganda", "Restez proche de ceux qui comptent."),
        ("build-your-future.jpg", "Construire demain", "Accompagner vos projets en RDC."),
        ("closer-to-family.jpg", "Garder le lien", "Être présent, même à distance."),
        ("uganda-connections.jpg", "Aller plus loin", "De nouveaux horizons avec Blue Sky."),
        ("horizons.jpg", "Votre avenir, notre engagement", "Un accompagnement pour vos ambitions."),
        ("your-ambitions.jpg", "Donner vie à vos idées", "Vos projets voyagent avec vous."),
        ("billboard.jpg", "Blue Sky à vos côtés", "Découvrez notre campagne de transfert."),
    ]
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "campaigns": campaigns})


def post_detail(request, slug):
    if request.user.is_authenticated and request.user.is_staff:
        post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    else:
        post = get_object_or_404(
            Post.objects.select_related("author"), slug=slug, is_published=True
        )
    return render(request, "blog/post_detail.html", {"post": post})
