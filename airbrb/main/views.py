from re import search
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .athena import pedirCosas, pedirCosas2, pedirCosaGenerica
from .query import query_agreggator
from .models import Query
from django.db.models import Sum
from django.http import JsonResponse
from random import randint
# Create your views here.

def home(response):
	return render(response, "main/home.html", {})
	#return HttpResponse("OK")

def index(response):
	return render(response, "main/index.html", {})
	#return HttpResponse("OK")


# def graph(response):
# 	labels = []
# 	data = []
# 	rColours = []
    
# 	for row in pedirCosas("price<50")[1:]:
# 		labels.append(row[0])
# 		data.append(row[1])
# 		rColours.append([randint(0,255),randint(0,255),randint(0,255)])
    
# 	return render(response, "main/graph.html", {"labels":labels,"data":data,"rColours":rColours})


# def graph2(response):
# 	showData = []
# 	for row in pedirCosas("price<50")[1:]:
# 		showData.append([row[0],row[1], randint(0,255),randint(0,255),randint(0,255)])
# 	print(showData)
# 	return render(response, "main/graph2.html", {"showData":showData})

# def graph3(response):
# 	dictCountries = {}
# 	randColors = []
    
# 	for row in pedirCosas2()[1:]:
# 		color1 = randint(0,255)
# 		color2 = randint(0,255)
# 		color3 = randint(0,255)
        
# 		if (row[0] not in dictCountries):
# 			dictCountries[row[0]] = []
# 			dictCountries[row[0]].append('rgba('+str(color1)+','+str(color2)+','+str(color3)+',0.8)') 
# 			#randColors.append('rgba('+str(color1)+','+str(color2)+','+str(color3)+',1)') 
        
# 		dictCountries[row[0]].append([row[1],row[2]])
	
# 	return render(response, "main/graph3.html", {"dictCountries":dictCountries,"randColors":randColors})

# def graph4(response):

# 	query = []
# 	query.append("select amsterdam_unido_.procedence, amsterdam_lista_reducida_.number_of_reviews, avg(amsterdam_unido_.price) from amsterdam_lista_reducida_ join amsterdam_unido_ on amsterdam_lista_reducida_.id = amsterdam_unido_.listing_id group by amsterdam_lista_reducida_.number_of_reviews, amsterdam_unido_.procedence ")
# 	query.append("select berlin_unido_.procedence, berlin_lista_reducida_.number_of_reviews, avg(berlin_unido_.price) from berlin_lista_reducida_ join berlin_unido_ on berlin_lista_reducida_.id = berlin_unido_.listing_id group by berlin_lista_reducida_.number_of_reviews, berlin_unido_.procedence ")
# 	query.append("select edinburgh_unido_.procedence, edinburgh_lista_reducida_.number_of_reviews, avg(edinburgh_unido_.price) from edinburgh_lista_reducida_ join edinburgh_unido_ on edinburgh_lista_reducida_.id = edinburgh_unido_.listing_id group by edinburgh_lista_reducida_.number_of_reviews, edinburgh_unido_.procedence ")
# 	query.append("select istambul_.procedence, istambul_lista_reducida_.number_of_reviews, avg(istambul_.price) from istambul_lista_reducida_ join  istambul_ on istambul_lista_reducida_.id = istambul_.listing_id WHERE istambul_lista_reducida_.number_of_reviews IS NOT NULL group by  istambul_lista_reducida_.number_of_reviews, istambul_.procedence  ")
# 	query.append("select madrid_unido_.procedence, madrid_lista_reducida_.number_of_reviews, avg(madrid_unido_.price) from madrid_lista_reducida_ join madrid_unido_ on madrid_lista_reducida_.id = madrid_unido_.listing_id group by madrid_lista_reducida_.number_of_reviews, madrid_unido_.procedence ")
# 	query.append("select paris_unido_.procedence, paris_lista_reducida_.number_of_reviews, avg(paris_unido_.price) from paris_lista_reducida_ join paris_unido_ on paris_lista_reducida_.id = paris_unido_.listing_id group by paris_lista_reducida_.number_of_reviews, paris_unido_.procedence ")
# 	query.append("select rio_unido_.procedence, rio_lista_reducida_.number_of_reviews, avg(rio_unido_.price) from rio_lista_reducida_ join rio_unido_ on rio_lista_reducida_.id = rio_unido_.listing_id group by rio_lista_reducida_.number_of_reviews, rio_unido_.procedence ")
# 	query.append("select sydney_unido_.procedence, sydney_lista_reducida_.number_of_reviews, avg(sydney_unido_.price) from sydney_lista_reducida_ join sydney_unido_ on sydney_lista_reducida_.id = sydney_unido_.listing_id group by sydney_lista_reducida_.number_of_reviews, sydney_unido_.procedence ")
# 	query.append("select tokio_unido_.procedence, tokio_lista_reducida_.number_of_reviews, avg(tokio_unido_.price) from tokio_lista_reducida_ join tokio_unido_ on tokio_lista_reducida_.id = tokio_unido_.listing_id group by tokio_lista_reducida_.number_of_reviews, tokio_unido_.procedence ")
    
# 	dictCountries = {}
    
# 	for q in query:
# 		for row in pedirCosaGenerica(q)[1:]:
# 			color1 = randint(0,255)
# 			color2 = randint(0,255)
# 			color3 = randint(0,255)
            
# 			if (row[0] not in dictCountries):
# 				dictCountries[row[0]] = []
# 				dictCountries[row[0]].append('rgba('+str(color1)+','+str(color2)+','+str(color3)+',0.8)') 

# 			dictCountries[row[0]].append([row[1],row[2]])
	
# 	return render(response, "main/graph3.html", {"dictCountries":dictCountries})



def city(response):
	return render(response, "main/city.html", {})


def options(response):
	#	context = {}
	#	system = response.POST.get('system', None)
	#	context['system'] = system
	#	return render(response, "main/options.html", context)
	search = Query()
	search.city = response.GET.get('city', None)
	search.min = response.GET.get('max', None)
	search.max = response.GET.get('min', None)
	if search.max < search.min:
		aux = search.min
		search.min = search.max
		search.max = aux
	city = "{0}".format(search.city.lower())
	rango_precio = "{}<price AND price<{}".format(search.min,search.max)
	query = []
	if city == "istambul":
		query.append("SELECT neighbourhood, Count(price) FROM {1}_lista_reducida_ JOIN {1}_       ON {1}_lista_reducida_.id = {1}_.listing_id       WHERE {0} AND neighbourhood IS NOT NULL  GROUP BY neighbourhood".format(rango_precio, city))
	else:
		query.append("SELECT neighbourhood, Count(price) FROM {1}_lista_reducida_ JOIN {1}_unido_ ON {1}_lista_reducida_.id = {1}_unido_.listing_id WHERE {0} AND neighbourhood IS NOT NULL  GROUP BY neighbourhood".format(rango_precio, city))

	showData = []
	for row in pedirCosaGenerica(query[0])[1:]:
		showData.append([row[0],row[1], randint(0,255),randint(0,255),randint(0,255)])

	return render(response, "main/citydetail.html", {"showData": showData})

def something(response):
	search = Query()
	search.city = response.GET.get('city', None)
	search.limit = response.GET.get('limit', None)
	return render(response, "main/something.html", {'search': search})

def cityBudget(response):

	dato = response.GET.get('city','')

	#Opciones A, tapar en ifs
	#Opcion B, hacer un diccionario con los query y pasarle cuidad como key
	query = []
	query.append("SELECT neighbourhood, Count(price) FROM amsterdam_lista_reducida_ JOIN amsterdam_unido_ ON amsterdam_lista_reducida_.id = amsterdam_unido_.listing_id WHERE price<=50 GROUP BY neighbourhood")

	showData = []
	for row in pedirCosaGenerica(query[0])[1:]:
		showData.append([row[0],row[1], randint(0,255),randint(0,255),randint(0,255)])

	return render(response, "main/citydetail.html", {"showData": showData})

def AllCitiesGraphs(response):
	search = Query()
	search.min = response.GET.get('min', None)
	search.max = response.GET.get('max', None)
	if search.max < search.min:
		aux = search.min
		search.min = search.max
		search.max = aux
	rango_precio = "{}<price AND price<{}".format(search.min,search.max)
	#Data Dona -- usa rango de precios 
	labels_dona = []
	data_dona = []
	rColours_dona = []
    
	#Data Barras verticales -- usa rango de precios 
	showData = []
    
	for row in pedirCosas(rango_precio)[1:]:
		c1 = randint(0,255)
		c2 = randint(0,255)
		c3 = randint(0,255)
		labels_dona.append(row[0])
		data_dona.append(row[1])
		rColours_dona.append([c1,c2,c3])
		showData.append([row[0],row[1], c1,c2,c3])
    
	#Data Scatter -- usa promedio de precios
	query = []
	query.append("select amsterdam_unido_.procedence, amsterdam_lista_reducida_.number_of_reviews, avg(amsterdam_unido_.price) from amsterdam_lista_reducida_ join amsterdam_unido_ on amsterdam_lista_reducida_.id = amsterdam_unido_.listing_id WHERE amsterdam_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<amsterdam_unido_.price AND amsterdam_unido_.price<{1}) group by amsterdam_lista_reducida_.number_of_reviews, amsterdam_unido_.procedence  ".format(search.min,search.max))
	query.append("select berlin_unido_.procedence, berlin_lista_reducida_.number_of_reviews, avg(berlin_unido_.price) from berlin_lista_reducida_ join berlin_unido_ on berlin_lista_reducida_.id = berlin_unido_.listing_id WHERE berlin_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<berlin_unido_.price AND berlin_unido_.price<{1}) group by berlin_lista_reducida_.number_of_reviews, berlin_unido_.procedence  ".format(search.min,search.max))
	query.append("select edinburgh_unido_.procedence, edinburgh_lista_reducida_.number_of_reviews, avg(edinburgh_unido_.price) from edinburgh_lista_reducida_ join edinburgh_unido_ on edinburgh_lista_reducida_.id = edinburgh_unido_.listing_id WHERE edinburgh_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<edinburgh_unido_.price AND edinburgh_unido_.price<{1}) group by edinburgh_lista_reducida_.number_of_reviews, edinburgh_unido_.procedence  ".format(search.min,search.max))		
	query.append("select istambul_.procedence, istambul_lista_reducida_.number_of_reviews, avg(istambul_.price) from istambul_lista_reducida_ join istambul_ on istambul_lista_reducida_.id = istambul_.listing_id WHERE istambul_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<istambul_.price AND istambul_.price<{1}) group by istambul_lista_reducida_.number_of_reviews, istambul_.procedence  ".format(search.min,search.max))
	query.append("select madrid_unido_.procedence, madrid_lista_reducida_.number_of_reviews, avg(madrid_unido_.price) from madrid_lista_reducida_ join madrid_unido_ on madrid_lista_reducida_.id = madrid_unido_.listing_id WHERE madrid_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<madrid_unido_.price AND madrid_unido_.price<{1}) group by madrid_lista_reducida_.number_of_reviews, madrid_unido_.procedence  ".format(search.min,search.max))
	query.append("select paris_unido_.procedence, paris_lista_reducida_.number_of_reviews, avg(paris_unido_.price) from paris_lista_reducida_ join paris_unido_ on paris_lista_reducida_.id = paris_unido_.listing_id WHERE paris_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<paris_unido_.price AND paris_unido_.price<{1}) group by paris_lista_reducida_.number_of_reviews, paris_unido_.procedence  ".format(search.min,search.max))
	query.append("select rio_unido_.procedence, rio_lista_reducida_.number_of_reviews, avg(rio_unido_.price) from rio_lista_reducida_ join rio_unido_ on rio_lista_reducida_.id = rio_unido_.listing_id WHERE rio_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<rio_unido_.price AND rio_unido_.price<{1}) group by rio_lista_reducida_.number_of_reviews, rio_unido_.procedence  ".format(search.min,search.max))
	query.append("select sydney_unido_.procedence, sydney_lista_reducida_.number_of_reviews, avg(sydney_unido_.price) from sydney_lista_reducida_ join sydney_unido_ on sydney_lista_reducida_.id = sydney_unido_.listing_id WHERE sydney_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<sydney_unido_.price AND sydney_unido_.price<{1}) group by sydney_lista_reducida_.number_of_reviews, sydney_unido_.procedence  ".format(search.min,search.max))
	query.append("select tokio_unido_.procedence, tokio_lista_reducida_.number_of_reviews, avg(tokio_unido_.price) from tokio_lista_reducida_ join tokio_unido_ on tokio_lista_reducida_.id = tokio_unido_.listing_id WHERE tokio_lista_reducida_.number_of_reviews IS NOT NULL AND ({0}<tokio_unido_.price AND tokio_unido_.price<{1}) group by tokio_lista_reducida_.number_of_reviews, tokio_unido_.procedence  ".format(search.min,search.max))
	
	dictCountries = {}
    
	for q in query:
		for row in pedirCosaGenerica(q)[1:]:
			color1 = randint(0,255)
			color2 = randint(0,255)
			color3 = randint(0,255)
            
			if (row[0] not in dictCountries):
				dictCountries[row[0]] = []
				dictCountries[row[0]].append('rgba('+str(color1)+','+str(color2)+','+str(color3)+',0.8)') 
			dictCountries[row[0]].append([row[1],row[2]])
    
	return render(response, "main/AllCitiesGraphs.html", {"labels":labels_dona,"data":data_dona,"rColours":rColours_dona, "showData":showData, "dictCountries":dictCountries} )
