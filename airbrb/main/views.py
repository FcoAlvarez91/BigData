from django.shortcuts import render
from django.http import HttpResponse
from .athena import pedirCosas

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

"""
def random_int(a, b=None):
	if b is None:
		a, b = 0, a
	return random.randint(a,b)
"""