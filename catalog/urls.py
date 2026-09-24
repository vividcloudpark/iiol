from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/search/", views.search, name="search"),
    path("api/regions/", views.regions, name="regions"),
]
