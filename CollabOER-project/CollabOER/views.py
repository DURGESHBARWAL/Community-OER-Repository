from django.shortcuts import render
from django.contrib import messages


from django.views.generic import View
from django.utils import timezone
from .render import Render
from random import *
from decimal import Decimal


import requests


class Pdf(View):

	def get(self,request):
		articles = [{"title":"Welcome to DSpace", "author":"Manu Nagar", "community": "DSace", "body": "The human body is the entire structure of a human being. It is composed of many different types of cells that together create tissues and subsequently organ systems. They ensure homeostasis and the viability of the human body.It comprises a head, neck, trunk (which includes the thorax and abdomen), arms and hands, legs and feet.The study of the human body involves anatomy, physiology, histology and embryology. The body varies anatomically in known ways. Physiology focuses on the systems and organs of the human body and their functions. Many systems and mechanisms interact in order to maintain homeostasis, with safe levels of substances such as sugar and oxygen in the blood.The body is studied by health professionals, physiologists, anatomists, and by artists to assist them in their work." }]
		today = timezone.now()
		print(today)
		params = {
       		'today': today,
        	'articles': articles,
    	}
		return Render.render('pdf.html', params)



def homepage(request):
	return render(request,'home.html')

# Test functions for CC
def test_get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')
	data = r.json()
	print(data)
	for name in data:
		print(name['name'])		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetched all Communities from Collaboration System')
	else:
		messages.error(request, 'Error in Fetching the Communities from Collaboration System')	
	return render(request,'home.html',{'data':data})


def test_get_community_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/communityarticlesapi/')
	data = r.json()
	print(data)
	for name in data:
		print(name['title'])
		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetched all Resources of Communities from CC')
	else:
		messages.error(request, 'Error in Fetching the Resources of Communities from CC')
	return render(request,'home.html',{'data1':data})



def test_get_groups(request):
	r = requests.get('http://localhost:8000/api/dspace/groupapi/')	
	data = r.json()
	print(data)
		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetched all Groups of Communities from CC')
	else:
		messages.error(request, 'Error in Fetching Groups of Communities from CC')
	return render(request,'home.html')

def test_get_group_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/grouparticlesapi/')	
	data = r.json()
	print(data)
		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetched all Resources of Group from CC')
	else:
		messages.error(request, 'Error in Fetching Groups Resources of Group from CC')
	return render(request,'home.html')




def test_login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		messages.success(request, 'User Successfully Logged in to the DSpace System')
	else:
		messages.error(request, 'Error in Login to DSpace System')	
	return render(request,'home.html')

	
def test_logout(request):
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		messages.success(request, 'User Successfully Logged out from the DSpace System.')
	else:
		message.error(request, 'Error in Logout from DSpace System')
	return render(request,'home.html')



def test_create_collection(request):

	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a community
	community_name = "Hello"
	uuid=0
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	#login
	sessionid = test_login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	
	
	#Creation of Sub Community
	if uuid!=0:
		url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
		head = {'Content-Type': 'application/json'}
		data = { 
		"name": "A Collection",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": ""}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
	
		r = requests.post(url, headers=head, json=data, cookies = jar)
		if r.status_code==200:
			messages.success(request, 'Collection is Created Successfully')
		else: 
			messages.error(request, 'Error in Collection Creation')
	else:
		messages.error(request,'Top Level Community Not Found')
	#logout
	logout(request)
	return render(request,'home.html')




def test_create_sub_community(request):
	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a community
	community_name = "Hello"
	uuid=0
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			

	#login
	sessionid = login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	

	#Creation of Sub Community
	if uuid != 0:	
		url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
		head = {'Content-Type': 'application/json'}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
		r = requests.post(url, headers=head, json={ 
		"name": "FIFA World Cup",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": ""}, cookies = jar)
		if r.status_code==200:
			messages.success(request, 'Sub-Community is Created Successfully')
		else: 
			messages.error(request, 'Error in Sub-Community Creation')
	else:
		messages.error(request, 'Top Level Community Not Found')
	
	#logout	
	logout(request)
	return render(request,'home.html')




#################################################################################################################

#Main Functions

def get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')	
	data = r.json()
	print(data)
	for name in data:
		print(name['name'])
		
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Communities from Collaboration System')
		return data
	elif r.status_code==200:
		messages.success(request, 'No Communities to Fetch from Collaboration System')
		return 0
	else:
		messages.error(request, 'Error in Fetching the Communities from Collaboration System')
		return 0


def get_community_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/communityarticlesapi/')
	
	data = r.json()
	print(data)
	for name in data:
		print(name['title'])
		
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Resources of Communities from Collaboration System')
		return data
	elif r.status_code==200:
		messages.success(request, 'No Resources to Fetch from Collaboration System')
		return 0
	else: 		
		messages.error(request, 'Error in Fetching the Resources of Communities from Collaboration System')
		return 0

def login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		messages.success(request, 'User Successfully Logged in to the DSpace System')
		return sessionid
	else:
		messages.error(request, 'Error in Login to DSpace System')
		return 500

def logout(request):
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		messages.success(request, 'User Successfully Logged out from the DSpace System.')
		return 1
	else:
		message.error(request, 'Error in Logout from DSpace System')
		return 0


def create_collection(request, collection, community, jar):
	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	r = requests.get(url, headers = {'Content-Type': 'application/json'})
        
	#Getting the uuid of a community
	community_name = collection
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	
	#Creation of Sub Community
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
		
	r = requests.post(url, headers=head, json=community, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'Collection is Created Successfully')
	else: 
		messages.error(request, 'Error in Collection Creation')




def create_community(request):        
	#login funcion calling
	sessionid = login(request)
	if sessionid != 500:
		#User Successfully Login to the System
		#Community POST
		url = 'http://127.0.0.1:80/rest/communities'
		head = {'Content-Type': 'application/json'}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
		k=100
		#Getting all the Communities from CC
		data=get_communities(request)
		if data!=0:
			for name in data:
				while(k==100):
					community={"name": name['name'],"copyrightText": "","introductoryText": "","shortDescription": name['desc'],"sidebarText": ""}
					r = requests.post(url, headers=head, json=community, cookies = jar)
					if r.status_code==200:
						messages.success(request, 'Community is Created Successfully')
						create_collection(request,name['name'],community,jar)        
						k=200
					else: 
						k=100				
						messages.error(request, 'Error in Community Creation')
				k=100			
		#logout
		logout(request)
	return render(request,'home.html')



def create_community_resources(request):
	data=get_community_resources(request) 
	if data!=0: 
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for name in data:			        
				#Getting the uuid of a collection
				collection_name = name['cname']
				uuid=0
				for i in r.json():
					if collection_name==i['name']:
						uuid=i['uuid']
						exit			
				#Addition of an item in a collection
				if uuid != 0:	
					url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
					item = {"metadata":[
			{
			"key": "dc.contributor.author",
			"value": "Sinha, Hariom"
			},
			{
			"key": "dc.description",
			"language": "pt_BR",
			"value": "This article is usefull for the Sports team."
			},
			{
			"key": "dc.description.abstract",
			"language": "pt_BR",
			"value": "Another thing to note is that there are Query Parameters that you can tack on to the end of an endpoint to do extra things. The most commonly used one in this API. Instead of every API call defaulting to giving you every possible piece of information about it, it only gives a most commonly used set by default and gives the more information when you deliberately request it."
			},
			{
			"key": "dc.title",
			"language": "pt_BR",
			"value": "Basics of VollyBall"
			},
			{
			"key": "dc.date.issued",
			"value": "2018-05-03",
			"language": "en_US"
			},
			{
			"key": "dc.publisher",
			"value": "Mad Hostel",
			"language": "en_US"
			}]}
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if r.status_code==200:
						messages.success(request, 'Item is Created Successfully in DSpace')
						create_bitstream(request, data['title'], item, jar)
					else: 
						messages.error(request, 'Error in Item POSTing to DSpace')	
		if sessionid!=500:
			#logout
			logout(request)		
	return render(request,'home.html')

def create_bitstream(request, title, data, jar):	
	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	r = requests.get(url, headers={'Content-Type': 'application/json'})
        
	#Getting the uuid of a Item
	item_name = title
	for i in r.json():
		if item_name==i['name']:
			uuid=i['uuid']
			exit			

	#Addition of an Bitstream in a item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	data = {"name": "5th_presentation.pdf", "description": "good"}
	
	files = {'file': open('/home/dspace/Downloads/Project05_Presentation_04_2018_06_01.pdf', 'rb')}

	r = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'File is Inserted Successfully')
	else: 
		messages.error(request, 'Error in File Insertion Creation')


#######################################################################3

def test_create_community_resources(request):

	#get community resources
	data=[{"articleid":"5","title":"Hariom Nagar ", "author":"Manu Nagar", "community": "DSace", "body": "The human body is the entire structure of a human being. It is composed of many different types of cells that together create tissues and subsequently organ systems. They ensure homeostasis and the viability of the human body.It comprises a head, neck, trunk (which includes the thorax and abdomen), arms and hands, legs and feet.The study of the human body involves anatomy, physiology, histology and embryology. The body varies anatomically in known ways. Physiology focuses on the systems and organs of the human body and their functions. Many systems and mechanisms interact in order to maintain homeostasis, with safe levels of substances such as sugar and oxygen in the blood.The body is studied by health professionals, physiologists, anatomists, and by artists to assist them in their work.","cname":"School of Civil Engineering" }]

 
	if data!=0: 
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for name in data:			        
				#Getting the uuid of a collection
				collection_name = name['cname']
				uuid=0
				for i in r.json():
					if collection_name==i['name']:
						uuid=i['uuid']
						exit			
				#Addition of an item in a collection
				if uuid != 0:	
					url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
					item = {"metadata":[
			{
			"key": "dc.contributor.author",
			"value": name['author']
			},
			{
			"key": "dc.description",
			"language": "pt_BR",
			"value": "This article is usefull for the Sports team."
			},
			{
			"key": "dc.title",
			"language": "pt_BR",
			"value": name['title']
			},
			{
			"key": "dc.date.issued",
			"value": "2018-05-03",
			"language": "en_US"
			},
			{
			"key": "dc.publisher",
			"value": "Mad Hostel",
			"language": "en_US"
			}]}
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if r.status_code==200:
						messages.success(request, 'Item is Created Successfully in DSpace')
						print(name['title'])
						print(name)
						test_create_bitstream(request, name['title'], name, sessionid)
					else: 
						messages.error(request, 'Error in Item POSTing to DSpace')	
		if sessionid!=500:
			#logout
			logout(request)		
	return render(request,'home.html')

def test_create_bitstream(request, title, name, sessionid):	
	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	r = requests.get(url, headers={'Content-Type': 'application/json'})
        
	
	#Getting the uuid of a Item
	item_name=title
	for i in r.json():
		if (item_name and i['name']):
			uuid=i['uuid']
			exit

	#Addition of an Bitstream in a item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	data = {"name": "5th_presentation.pdf", "description": "good"}
	
	print(url)

	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
	
	#files = {'file': open('/home/dspace/Downloads/Project05_Presentation_04_2018_06_01.pdf', 'rb')}
				
	abc=getpdf(request, name)
	files = {'file': open('Files/temp'+ str(name['articleid']) +'.pdf', 'rb')}
	#files = {'file': open("abc", 'rb')}
	
	r = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'File is Inserted Successfully')
	else: 
		messages.error(request, 'Error in File Insertion Creation')


def getpdf(request, name):
		#article=[name]		
		#articles = [{"title":"Hello", "author":"Manu Nagar", "community": "DSace", "body": "The human body is the entire structure of a human being. It is composed of many different types of cells that together create tissues and subsequently organ systems. They ensure homeostasis and the viability of the human body.It comprises a head, neck, trunk (which includes the thorax and abdomen), arms and hands, legs and feet.The study of the human body involves anatomy, physiology, histology and embryology. The body varies anatomically in known ways. Physiology focuses on the systems and organs of the human body and their functions. Many systems and mechanisms interact in order to maintain homeostasis, with safe levels of substances such as sugar and oxygen in the blood.The body is studied by health professionals, physiologists, anatomists, and by artists to assist them in their work." }]
		

		#year = article['created_at'][:4]
		#month = article['created_at'][5:7]
		#day = article['created_at'][8:10]
		#hours = article['created_at'][11:13]
		#minutes = article['created_at'][14:16]
		#seconds = article['created_at'][17:19]
		#date = day+"/"+month+"/"+year+" "+hours+":"+minutes+":"+seconds
		filename = "temp"+str(name['articleid'])+".pdf"
		params = {
			'title': name['title'],
			'body' : name['body'],
			'created_by': name['author'],
			'cname': name['cname'],
			}
	
		x = Render.render('pdf.html',params, filename, name['cname'])
		return x

	
