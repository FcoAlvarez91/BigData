from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("graph/", views.graph, name="graph"),
path("index/", views.index, name="index"),
path("city/", views.city, name="city"),
path("city/options/", views.options, name="options"),
path("city/options/something/", views.something, name="something"),
path("graph2/", views.graph2, name="graph2"),
]