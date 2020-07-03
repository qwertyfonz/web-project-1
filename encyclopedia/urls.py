from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.page, name="page")
]