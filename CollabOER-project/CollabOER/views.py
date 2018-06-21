from django.shortcuts import render
from django.contrib import messages


from django.views.generic import View
from django.utils import timezone
from .render import Render
from random import *
from decimal import Decimal


import requests


def homepage(request):
	return render(request,'home.html')

# Test functions for CC
def test_get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')
	data = r.json()	
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Communities from Collaboration System')
	elif r.status_code==200:
		messages.success(request, 'No Communities to Fetch from Collaboration System')
	else:
		messages.error(request, 'Error in Fetching the Communities from Collaboration System')	
	return render(request,'home.html',{'data':data})

def test_get_community_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/communityarticlesapi/')
	data = r.json()
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Resources of Communities from Collaboration System')
	elif r.status_code==200:
		messages.success(request, 'No Resources to Fetch from Collaboration System')
	else: 		
		messages.error(request, 'Error in Fetching the Resources of Communities from Collaboration System')
	return render(request,'home.html',{'data1':data})



def test_get_groups(request):
	r = requests.get('http://localhost:8000/api/dspace/groupapi/')	
	data = r.json()
	if (r.status_code==200  and data):	
		messages.success(request, 'Successfully Fetched all Groups of Communities from Collaboration System')
	elif r.status_code==200:
		messages.success(request, 'No Groups to Fetch from Collaboration System')
	else:
		messages.error(request, 'Error in Fetching Groups of Communities from Collaboration System')
	return render(request,'home.html')

def test_get_group_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/grouparticlesapi/')	
	data = r.json()
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Resources of Group from Collaboration System')
	elif r.status_code==200:
		messages.success(request, 'No Resources of Group to Fetch from Collaboration System')
	else:
		messages.error(request, 'Error in Fetching Groups Resources of Group from Collaboration System')
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




#################################################################################################################

#Main Functions

def get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')	
	data = r.json()
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
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Resources of Communities from Collaboration System')
		return data
	elif r.status_code==200:
		messages.success(request, 'No Resources to Fetch from Collaboration System')
		return 0
	else: 		
		messages.error(request, 'Error in Fetching the Resources of Communities from Collaboration System')
		return 0


def get_groups(request):
	r = requests.get('http://localhost:8000/api/dspace/groupapi/')	
	data = r.json()
	if (r.status_code==200  and data):	
		messages.success(request, 'Successfully Fetched all Groups of Communities from Collaboration System')
		return data
	elif r.status_code==200:
		messages.success(request, 'No Groups to Fetch from Collaboration System')
		return 0
	else:
		messages.error(request, 'Error in Fetching Groups of Communities from Collaboration System')
		return 0

def get_groups_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/grouparticlesapi/')	
	data = r.json()
	if (r.status_code==200 and data):	
		messages.success(request, 'Successfully Fetched all Resources of Group from Collaboration System')
		return data
	elif r.status_code==200:
		messages.success(request, 'No Resources of Group to Fetch from Collaboration System')
		return 0		
	else:
		messages.error(request, 'Error in Fetching Groups Resources of Group from Collaboration System')
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


def create_collection(request, collection, community, jar, k):
	#Getting of all Communities
	if k==0:	
		url = 'http://127.0.0.1:80/rest/communities/top-communities'
	else:
		url = 'http://127.0.0.1:80/rest/communities'		
	r = requests.get(url, headers = {'Content-Type': 'application/json'})
        
	#Getting the uuid of a community
	community_name = collection
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	
	#Creation of Collection
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
		
	r = requests.post(url, headers=head, json=community, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'Collection is Created Successfully in DSpace')
	else: 
		messages.error(request, 'Error in Collection Creation in DSpace')




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
						create_collection(request,name['name'],community,jar,0)        
						k=200
					else: 
						k=100				
						messages.error(request, 'Error in Community Creation')
				k=100			
		#logout
		logout(request)
	return render(request,'home.html')


def create_groups(request):
	data=get_groups(request)
	if data!=0:
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Communities
			url = 'http://127.0.0.1:80/rest/communities/top-communities'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for group in data:
				#Getting the uuid of a community
				community_name = group['communityname'] #*****************
				for i in r.json():
					if community_name==i['name']:
						uuid=i['uuid']
						exit
				if uuid:
					url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
					content={ "name": group['name'], "copyrightText": "", "introductoryText": "Welcome to the Sport Club", "shortDescription": "This", "sidebarText": ""}
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json = content, cookies = jar)				#*********
					if r.status_code==200:
						messages.success(request, 'Group is Created in DSpace')
						#**************
						create_collection(request,group['name'],content,jar,1)
					else: 
						messages.error(request, 'Error in Group Creation in DSpace')
		if sessionid!=500:
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
				collection_name = name['communityname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				#Addition of an item in a collection
				if uuid != 0:	
					url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
					item = {"metadata":[
			{
			"key": "dc.contributor.author",
			"value": name['created_by']
			},
			{
			"key": "dc.title",
			"language": "pt_BR",
			"value": name['title']
			},
			{
			"key": "dc.date.issued",
			"value": name['published_on'],
			"language": "en_US"
			},
			{
			"key": "dc.publisher",
			"value": "Collaboration System",
			"language": "en_US"
			}]}
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if r.status_code==200:
						messages.success(request, 'Item is Created Successfully in DSpace')
						create_bitstream(request, name['title'], name, sessionid)
					else: 
						messages.error(request, 'Error in Item and File POSTing to DSpace')	
		if sessionid!=500:
			#logout
			logout(request)		
	return render(request,'home.html')



def create_groups_resources(request):
	data=get_groups_resources(request)
	if data!=0: 
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for name in data:			        
				#Getting the uuid of a collection
				collection_name = name['groupname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				#Addition of an item in a collection
				if uuid != 0:	
					url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
					item = {"metadata":[
			{
			"key": "dc.contributor.author",
			"value": name['created_by']
			},
			{
			"key": "dc.title",
			"language": "pt_BR",
			"value": name['title']
			},
			{
			"key": "dc.date.issued",
			"value": name['published_on'],
			"language": "en_US"
			},
			{
			"key": "dc.publisher",
			"value": "Collaboration System",
			"language": "en_US"
			}]}
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if r.status_code==200:
						messages.success(request, 'Item is Created Successfully in DSpace')
						create_group_bitstream(request, name['title'], name, sessionid)
					else: 
						messages.error(request, 'Error in Item and File POSTing to DSpace')	
		if sessionid!=500:
			#logout
			logout(request)		
	return render(request,'home.html')

def create_group_bitstream(request, title, name, sessionid):	
	
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
	filename = str(name['groupname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = get_grouparticle_pdf(request, name)
	files = {'file': open('Files/group'+ str(name['articleid']) +'.pdf', 'rb')}
	
	r = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'File is Inserted Successfully')
	else: 
		messages.error(request, 'Error in File Insertion Creation')


def get_grouparticle_pdf(request, name):
		
		filename = "group"+str(name['articleid'])+".pdf"
		params = {
			'title': name['title'],
			'body' : name['body'],
			'created_by': name['created_by'],
			'cname': name['groupname'],
			'published_on' : name['published_on']
			}
	
		x = Render.render('group_pdf.html',params, filename, name['groupname'])
		return x

def create_bitstream(request, title, name, sessionid):	
	
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
	filename = str(name['communityname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = getpdf(request, name)
	files = {'file': open('Files/temp'+ str(name['articleid']) +'.pdf', 'rb')}
	
	r = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'File is Inserted Successfully')
	else: 
		messages.error(request, 'Error in File Insertion Creation')


def getpdf(request, name):
		
		filename = "temp"+str(name['articleid'])+".pdf"
		params = {
			'title': name['title'],
			'body' : name['body'],
			'created_by': name['created_by'],
			'cname': name['communityname'],
			'published_on' : name['published_on']
			}
	
		x = Render.render('pdf.html',params, filename, name['communityname'])
		return x

	
