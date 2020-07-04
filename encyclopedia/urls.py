from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.page, name="page"),
    path("<str:entry>/editpage", views.editpage, name="editpage")
]