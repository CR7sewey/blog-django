from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Post

# Create your views here.
# posts = list(range(1000))

PER_PAGE = 9


def index(request):

    posts = Post.objects.get_published()  # type: ignore  # check models!
    # Put x number os contacts into each page
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, 'blog/pages/index.html', context,)


def post(request, slug):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    post = get_object_or_404(Post, is_published=True, slug=slug)

    # Put x number os contacts into each page
    # paginator = Paginator(posts, 9)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    context = {"post": post}
    return render(request, 'blog/pages/post.html', context,)


def page(request):
    # Put x number os contacts into each page

    context = {"page_obj": page_obj}
    return render(request, 'blog/pages/page.html', context,)
