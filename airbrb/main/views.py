from django.shortcuts import render
from django.http import HttpResponse
from .athena import pedirCosas

from django.db.models import Sum
from django.http import JsonResponse
# Create your views here.

def home(response):
	return render(response, "main/home.html", {})
	#return HttpResponse("OK")


def graph(response):
	labels = []
	data = []

	for row in pedirCosas()[1:]:
		labels.append(row[0])
		data.append(row[1])

	print("graph 1")

	return render(response, "main/graph.html", {"var1":123213,"labels":labels,"data":data})

	
def graph2(response):
	labels = []
	data = []
	
	for row in pedirCosas()[1:]:
		labels.append(row[0])
		data.append(row[1])

	return render(response, "main/graph2.html", {"var1":123213,"labels":labels,"data":data})