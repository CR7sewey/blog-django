from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.models import Category, Post, Page
from django.db.models import Q  # or
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.
# posts = list(range(1000))

PER_PAGE = 9


class PostListView(ListView):  # Class based view - ListView
    model = Post  # model a carregar
    template_name = 'blog/pages/index.html'  # template a renderizar
    # name with objects - in index is page_obj, aqui colide com o paginator
    context_object_name = 'posts'
    ordering = '-id',
    paginate_by = PER_PAGE
    # paginator_class = Paginator  - default
    queryset = Post.objects.get_published()

    # para query ou como em cima!
    # def get_queryset(self) -> QuerySet[Any]:
    #    queryset = super().get_queryset()
    #    queryset = queryset.filter(is_published=True)
    #    return queryset

    # se quiser mexer no contexto
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # metodo do dict para updatar
        context.update({"page_title": "Home - "})
        print(context)  # seeeeeeee the arguments!
        return context


'''
def index(request):

    posts = Post.objects.get_published()  # type: ignore  # check models!
    # Put x number os contacts into each page
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "page_title": "Home - "}
    return render(request, 'blog/pages/index.html', context,)
'''

'''
def post(request, slug):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    post_obj = get_object_or_404(Post, is_published=True, slug=slug)

    # Put x number os contacts into each page
    # paginator = Paginator(posts, 9)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    context = {"post": post_obj, "page_title": f'{post_obj.title} - Post - '}
    return render(request, 'blog/pages/post.html', context,)
'''


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context)
        context.update({"page_title":
                        f'{self.get_object().title} - Page - '})
        return context

    # este metodo pq queremso uma http response! - desnecessairo pq is_published ja faz!
    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

    #   get_object_or_404(Page, slug=self.kwargs.get("slug"))
    #   return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_published=True)  # desnecsasrio, slug=self.kwargs.get("slug"))
        return queryset


class PostDetailView(PageDetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    # slug_field = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context)
        context.update({"page_title":
                        f'{self.get_object().title} - Post - '})
        return context


'''
def page(request, slug):
    # Put x number os contacts into each page
    # ou Page-objects.filter(is_pub).filter(slug).first()
    page_obj = get_object_or_404(Page, is_published=True, slug=slug)

    context = {"page": page_obj, "page_title": f'{page_obj.title} - Page - '}
    return render(request, 'blog/pages/page.html', context,)
'''

'''
def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()
    if user is None:
        raise Http404('This user does\'nt exists!')

    user_full_name = user.username if not user.first_name else f'{
        user.first_name} {user.last_name}'
    user_full_name += ' posts - '

    # post = Post.objects.filter(is_published=True, slug=slug).first()
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj,
               "page_title": user_full_name}
    return render(request, 'blog/pages/index.html', context,)
'''


class CreatedByListView(PostListView):  # herdar de algo ja qs

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}  # contexto temporario

    # ha uma ordem em qual os metodos sao chamados
    # (setup, get, get_query_set etc ver doc)
    # tudo o passado via url esta no kwargs
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self._temp_context["page_title"]
        user_full_name = user.username if not user.first_name else f'{
            user.first_name} {user.last_name}'
        user_full_name += ' posts - '
        context.update({"page_title": user_full_name})
        return context

    # este metodo pq queremso uma http response!
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # tudo o passado via url esta no kwargs
        user = User.objects.filter(pk=self.kwargs.get('author_pk')).first()
        if user is None:
            raise Http404('This user does\'nt exists!')
            # could return redirect('blog:index')
        self._temp_context = {"page_title": user}
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(
            created_by__pk=self._temp_context["page_title"].pk)
        return queryset


class CategoryListView(PostListView):
    allow_empty = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    # ha uma ordem em qual os metodos sao chamados
    # (setup, get, get_query_set etc ver doc)
    # tudo o passado via url esta no kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # print("_____________________", self.object_list)  # tem os posts!
        context.update({"page_title":
                       f'{self.object_list[0].category.name}'  # type: ignore
                        f' - Category -'})
        return context

    # este metodo pq queremso uma http response!
    # allow empty!
    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #    # tudo o passado via url esta no kwargs
    #    posts = Post.objects.filter(category__slug=self.kwargs.get('slug'))
    #    if posts is None:
    #        raise Http404('This category does\'nt exist!')
    #        # could return redirect('blog:index')
    #    self._temp_context = {"category_name": posts[0].category.name}
    #    return super().get(request, *args, **kwargs)

    # isto é primeiro que o get_context_data
    def get_queryset(self) -> QuerySet[Any]:
        print('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
        queryset = super().get_queryset()
        queryset = queryset.filter(category__slug=self.kwargs.get('slug'))
        return queryset


'''
def category(request, slug):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if len(page_obj) == 0:
        raise Http404('This category does\'nt exist!')

    context = {"page_obj": page_obj,
               "page_title": f'{page_obj[0].category.name} - '}
    return render(request, 'blog/pages/index.html', context,)
'''


class TagListView(PostListView):
    allow_empty = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # print("_____________________", self.object_list)  # tem os posts!
        context.update({"page_title":
                       # type: ignore
                        f'{self.object_list[0].tags.first().name}'
                        f' - Tag -'})
        return context

    # isto é primeiro que o get_context_data
    def get_queryset(self) -> QuerySet[Any]:
        print('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
        queryset = super().get_queryset()
        queryset = queryset.filter(tags__slug=self.kwargs.get('slug'))
        return queryset


'''
def tag(request, slug):
    # post = Post.objects.filter(is_published=True, slug=slug).first()
    posts = Post.objects.get_published().filter(tags__slug=slug)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404('This tag does\'nt exist!')

    context = {"page_obj": page_obj,
               # Manager de volta dai o first
               "page_title": page_obj[0].tags.first().name}
    return render(request, 'blog/pages/index.html', context,)
'''


class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get("search", '').strip()
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        searched_value = self._search_value
        # print("_____________________", self.object_list)  # tem os posts!
        context.update({"search": searched_value,
                        "page_title":
                       f'{searched_value[:15]} - Search - '})
        return context

    # este metodo pq queremso uma http response e o request!

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # tudo o passado via url esta no kwargs
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

    # isto é primeiro que o get_context_data
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        searched_value = self._search_value
        queryset = queryset.filter(
            Q(title__icontains=searched_value) |
            Q(excert__icontains=searched_value) |
            Q(content__icontains=searched_value))[0:PER_PAGE]
        return queryset


'''
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

    context = {"page_obj": posts, "search": searched_value,
               "page_title": f'{searched_value[:15]} - Search - '}
    return render(request, 'blog/pages/index.html', context,)
'''
