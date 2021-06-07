from django.shortcuts import render
from django.http import HttpResponse, request
from .athena import pedirCosas
from .query import query_agreggator
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

	return render(response, "main/graph.html", {"var1":123213,"labels":labels,"data":data})

def country(response):
	return render(response, "main/country.html", {})

def options(response):
	context = {}
	if response.method == 'POST':	
		system = response.POST.get('system', None)
		context['system'] = system
	return render(response, "main/options.html", context)
	