from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    posts = Post.objects.filter(is_published=True).select_related("author")
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    if request.user.is_authenticated and request.user.is_staff:
        post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    else:
        post = get_object_or_404(
            Post.objects.select_related("author"), slug=slug, is_published=True
        )
    return render(request, "blog/post_detail.html", {"post": post})
