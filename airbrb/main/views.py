from django.shortcuts import render
from django.http import HttpResponse
from .athena import pedirCosas
# Create your views here.

def home(response):
	return render(response, "main/home.html", {})
	#return HttpResponse("OK")

def index(response):
	return render(response, "main/index.html", {})
	#return HttpResponse("OK")


def graph(response):
	labels = []
	data = []

	for row in pedirCosas()[1:]:
		labels.append(row[0])
		data.append(row[1])

	return render(response, "main/graph.html", {"var1":123213,"labels":labels,"data":data})