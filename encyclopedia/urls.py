from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("add", views.add, name="add"),
    path("edit/<str:title>", views.edit_function, name="edit"),
    path("delete/<str:title>", views.delete_function, name="delete"),
    path("search", views.Search_function, name="search"),
    path("random", views.random_function, name="random")
]
