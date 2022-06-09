from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:name>", views.entrypage, name="entrypage"),
    path("editpage/<str:name>", views.editpage, name="editpage"),
    path("newpage", views.newpage, name="newpage"),
    path("randpage", views.randpage, name="randpage"),
    path("search", views.search, name="search")  
]
