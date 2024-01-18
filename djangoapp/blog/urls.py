from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    # views tem de ser callable (dai as_view)
    path("", views.PostListView.as_view(), name='index'),

    # POSTS
    path("post/<slug:slug>", views.post, name='post'),
    path("created_by/<int:author_pk>",
         views.CreatedByListView.as_view(), name='created_by'),
    path("category/<slug:slug>",
         views.CategoryListView.as_view(), name='category'),
    path("tag/<slug:slug>", views.TagListView.as_view(), name='tag'),

    # PAGES
    path("page/<slug:slug>", views.page, name='page'),

    # Search
    path("search/", views.search, name='search'),
]
