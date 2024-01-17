from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name='index'),

    # POSTS
    path("post/<slug:slug>", views.post, name='post'),
    path("created_by/<int:author_pk>", views.created_by, name='created_by'),
    path("category/<slug:slug>", views.category, name='category'),

    # PAGES
    path("page/<slug:slug>", views.page, name='page'),

]
