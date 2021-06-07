from django.shortcuts import render
from django.http import HttpResponse
from .athena import pedirCosas
# Create your views here.

def home(response):
	return render(response, "main/home.html", {})
	#return HttpResponse("OK")


def graph(response):
	return render(response, "main/graph.html", {"var1":123213,"data":pedirCosas()})
	#return HttpResponse("OK")