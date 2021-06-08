from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("graph/", views.graph, name="graph"),
path("index/", views.index, name="index"),
path("city/", views.city, name="city"),
path("city/options/", views.options, name="options"),
path("city/options/something/", views.something, name="something"),
path("AllCitiesGraphs/", views.AllCitiesGraphs, name="AllCitiesGraphs"),
path("graph2/", views.graph2, name="graph2"),
path("graph3/", views.graph4, name="graph3"),
path("citydetail/", views.cityBudget, name="citydetail")
]