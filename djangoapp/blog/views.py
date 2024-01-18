from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q  # or

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


def page(request, slug):
    # Put x number os contacts into each page
    # ou Page-objects.filter(is_pub).filter(slug).first()
    page = get_object_or_404(Page, is_published=True, slug=slug)

    context = {"page": page}
    return render(request, 'blog/pages/page.html', context,)


def created_by(request, author_pk):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, 'blog/pages/index.html', context,)


def category(request, slug):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    posts = Post.objects.get_published().filter(category__slug=slug)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, 'blog/pages/index.html', context,)


def tag(request, slug):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    posts = Post.objects.get_published().filter(tags__slug=slug)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, 'blog/pages/index.html', context,)


def search(request):
    searched_value = request.GET.get("search", '').strip()  # query
    print('---------------------', searched_value)
    if searched_value == '':
        # if none back to first page
        return redirect('blog:index')
    posts = Post.objects.get_published().filter(
        # Q(tags__icontains=searched_value) | # nao da com foreign keys assim
        # Q(category__icontains=searched_value) |
        Q(title__icontains=searched_value) |
        Q(excert__icontains=searched_value) |
        Q(content__icontains=searched_value))[0:PER_PAGE]
    # Q(created_by__icontains=searched_value))[0:PER_PAGE]

    # RETIREI PARA NAO TER MUITOS POSTS!
    # paginator = Paginator(posts, PER_PAGE)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    context = {"page_obj": posts, "search": searched_value}
    return render(request, 'blog/pages/index.html', context,)
