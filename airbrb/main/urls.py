from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("graph/", views.graph, name="graph"),
path("country/", views.country, name="country"),
path("country/options/", views.options, name="options"),
]