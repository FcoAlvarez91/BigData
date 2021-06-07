from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("graph/", views.graph, name="graph"),
path("graph2/", views.graph2, name="graph2"),
]