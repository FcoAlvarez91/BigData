from django.shortcuts import render
from django.http import HttpResponse, request
from .athena import pedirCosas
from .query import query_agreggator
from .models import Query
from django.db.models import Sum
from django.http import JsonResponse
from random import randint
# Create your views here.

def home(response):
	return render(response, "main/home.html", {})
	#return HttpResponse("OK")


def graph(response):
	labels = []
	data = []
	rColours = []

	for row in pedirCosas()[1:]:
		labels.append(row[0])
		data.append(row[1])
		rColours.append([randint(0,255),randint(0,255),randint(0,255)])

	print("graph 1")

	return render(response, "main/graph.html", {"labels":labels,"data":data,"rColours":rColours})

	
def graph2(response):
	showData = []
	
	for row in pedirCosas()[1:]:
		showData.append([row[0],row[1], randint(0,255),randint(0,255),randint(0,255)])
	print(showData)


	return render(response, "main/graph2.html", {"showData":showData})

def city(response):
	return render(response, "main/city.html", {})

def options(response):
#	context = {}
#	system = response.POST.get('system', None)
#	context['system'] = system
#	return render(response, "main/options.html", context)
	search = Query()
	search.city = response.POST.get('city', None)
	return render(response, "main/options.html", {'search': search})	

def something(response):
	search = Query()
	search.city = response.POST.get('city', None)
	search.limit = response.POST.get('limit', None)
	return render(response, "main/something.html", {'search': search})
