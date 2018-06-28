from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View
from django.utils import timezone
from .render import Render
from random import *
from decimal import Decimal


import requests


def home_page(request):
	return render(request,'home.html')

##################################Main Functions

def get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')	
	data = r.json()
	if (r.status_code==200 and data):	
		return data
	elif r.status_code==200:
		return 1
	else:
		return 0


def get_community_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/communityarticlesapi/')
	
	data = r.json()
	if (r.status_code==200 and data):	
		return data
	elif r.status_code==200:
		return 1
	else: 		
		return 0


def get_groups(request):
	r = requests.get('http://localhost:8000/api/dspace/groupapi/')	
	data = r.json()
	if (r.status_code==200  and data):	
		return data
	elif r.status_code==200:
		return 1
	else:
		return 0

def get_groups_resources(request):
	r = requests.get('http://localhost:8000/api/dspace/grouparticlesapi/')	
	data = r.json()
	if (r.status_code==200 and data):	
		return data
	elif r.status_code==200:
		return 1		
	else:
		return 0


def login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		return sessionid
	else:
		return 500

def logout(request):
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		return 1
	else:
		return 0


def create_community(request):        
	data=get_communities(request)
	if data!=0 and data!=1:
		message="Fetched --->"	
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			message+="Login --->"
			#Community POST
			url = 'http://127.0.0.1:80/rest/communities'
			head = {'Content-Type': 'application/json'}
			jar = requests.cookies.RequestsCookieJar()
			jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
			k=100
			count=0
			count_community=0;count_collection=0
			for name in data:
				count=count+1
				community={"name": name['name'], "copyrightText": "", "introductoryText": name['category'], "shortDescription": name['desc'], "sidebarText": ""}
				
				r = requests.post(url, headers=head, json=community, cookies = jar)
				if r.status_code==200:
					count_community = count_community + 1
					flag = create_collection(request, name['name'], community,jar,0)
					count_collection = count_collection + flag        
				else: 
					message += "Error in Community Creation --->" 
			message = str(count)+ " Communities " + message + " "+ str(count_community) + " Communties Created in DSpace" + " ---> " + str(count_collection) + " Collection is Created in DSpace "
			if count_community == count_collection:
				success_flag=1
			else: 
				success_flag=0	
		else:
			message="DSpace Login Failed"
			success_flag=0		
		if sessionid!=500:
			#logout
			if logout(request)==1:
			    message+="---> Logout"
			else:
			    message+="--> Error in Logout"    
	elif data==1:
		message="No Communities to Fetch"
		success_flag=1
	else:
		message="Error to Connect with Collaboration System"
		success_flag=0			
	content = {'msg': message, 'success_flag': success_flag}				
	return render(request,'home1.html', content)


def create_collection(request, collection, community, jar, k):
	#Getting all Communities
	if k==0:	
		url = 'http://127.0.0.1:80/rest/communities/top-communities'
	else:
		url = 'http://127.0.0.1:80/rest/communities'		
	res1 = requests.get(url, headers = {'Content-Type': 'application/json'})
        
	#Getting the uuid of a community
	community_name = collection
	for i in res1.json():
		if community_name == i['name']:
			uuid=i['uuid']
			exit				
	
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
	res2 = requests.post(url, headers=head, json=community, cookies = jar)
	if res2.status_code==200:
		return 1
	else: 
		return 0
	


				################## Community Articles ################


def create_community_resources(request):
	data=get_community_resources(request)
	if data!=0 and data!=1:
		message="Fetched --->"	
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			message+="Login --->"
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			count=0
			count_item=0;count_bitstream=0
			for name in data:
				count=count+1
				#Getting the uuid of a collection
				collection_name = name['communityname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				
				#Addition of an item in a collection
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
				response = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
				if response.status_code==200:
					count_item = count_item + 1
					flag = create_bitstream(request, name['title'], name, sessionid)
					count_bitstream = count_bitstream + flag        
				else: 
					message += "Error in Item and File Creation"
			message = str(count)+ " Articles " + message + " "+ str(count_item) + " Items Created in DSpace" + " ---> " + str(count_bitstream) + " Bitstream is Created in DSpace "
			if count_item == count_bitstream:
				success_flag=1
			else: 
				success_flag=0		
		else:
			message="---> Login Failed"
			success_flag=0		
		if sessionid!=500:
			#logout
			if logout(request)==1:
			    message+="---> Logout"
			else:
			    message+="--> Error in Logout"		
	elif data==1:
		message="No Communities Resources to Fetch"
		success_flag=1
	else:
		message="Error to Connect with Collaboration System"
		success_flag=0			
	content = {'msg': message, 'success_flag': success_flag}				
	return render(request,'home2.html', content)



def create_bitstream(request, title, name, sessionid):	
	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	res = requests.get(url, headers={'Content-Type': 'application/json'})
        
	
	#Getting the uuid of a Item
	item_name=title
	for i in res.json():
		if (item_name == i['name']):
			uuid=i['uuid']
			exit

	#Addition of an Bitstream in a item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	filename = str(name['communityname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = getpdf(request, name)
	files = {'file': open('Files/community'+ str(name['articleid']) +'.pdf', 'rb')}
	
	res = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if res.status_code==200:
		return 1
	else: 
		return 0


def getpdf(request, name):
		filename = "community"+str(name['articleid'])+".pdf"
		params = {
			'title': name['title'],
			'body' : name['body'],
			'created_by': name['created_by'],
			'cname': name['communityname'],
			'published_on' : name['published_on']
			}
		x = Render.render('pdf.html',params, filename, name['communityname'])
		return x







	
				############# GROUPS ###########################
def create_groups(request):
	data=get_groups(request)
	if data!=0 and data!=1:
		message="Fetched --->"	
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			message+="Login --->"
			#Getting of all Communities
			url = 'http://127.0.0.1:80/rest/communities/top-communities'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			count=0
			count_community=0;count_collection=0
			for group in data:
				count=count+1
				#Getting the uuid of a community
				community_name = group['community_name'] 
				for i in r.json():
					if community_name  == i['name']:
						uuid=i['uuid']
						exit
				url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
				head = {'Content-Type':'application/json'} 
				jar = requests.cookies.RequestsCookieJar()
				jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
				content1={ "name": group['name'], "copyrightText": "", "introductoryText": "", "shortDescription": group['desc'], "sidebarText": ""}
				re = requests.post(url,headers = head,json = content1, cookies = jar)			
				if re.status_code==200:
					count_community = count_community + 1
					flag = create_collection(request, group['community_name'], content1, jar, 1)
					count_collection = count_collection + flag        
				else: 
					message += "Error in Sub Community Creation --->" 
			message = str(count)+ " Groups " + message + " "+ str(count_community) + " Sub Communties Created in DSpace" + " ---> " + str(count_collection) + " Collection is Created in DSpace "
			if count_community == count_collection:
				success_flag=1
			else: 
				success_flag=0
					
					
		else:
			message="---> Login Failed"
			success_flag=0		
		if sessionid!=500:
			#logout
			if logout(request)==1:
			    message+="---> Logout"
			else:
			    message+="--> Error in Logout"		
	elif data==1:
		message="No Groups to Fetch"
		success_flag=1
	else:
		message="Error to Connect with Collaboration System"
		success_flag=0			
	content = {'msg': message, 'success_flag': success_flag}				
	return render(request,'home3.html', content)


				################# GROUPS RESOURCES #########################
def create_groups_resources(request):
		
	
	
	data=get_groups_resources(request)
	if data!=0 and data!=1: 
		message="Fetched --->"	
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			message+="Login --->"
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			count=0
			count_item=0;count_bitstream=0
			for name in data:			        
				count = count + 1
				#Getting the uuid of a collection
				collection_name = name['groupname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				#Addition of an item in a collection
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
				req = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
				if req.status_code==200:
					count_item = count_item + 1
					flag =create_group_bitstream(request, name['title'], name, sessionid)
					count_bitstream = count_bitstream + flag 
				else: 
					message += "Error in Item and File Creation"
			message = str(count)+ " Articles " + message + " "+ str(count_item) + " Items Created in DSpace" + " ---> " + str(count_bitstream) + " Bitstream is Created in DSpace "
			if count_item == count_bitstream:
				success_flag=1
			else: 
				success_flag=0	
		if sessionid!=500:
			#logout
			if logout(request)==1:
			    message+="---> Logout"
			else:
			    message+="--> Error in Logout"		
	elif data==1:
		message="No Group Resources to Fetch"
		success_flag=1
	else:
		message="Error to Connect with Collaboration System"
		success_flag=0			
	content = {'msg': message, 'success_flag': success_flag}				
	return render(request,'home4.html', content)


def create_group_bitstream(request, title, name, sessionid):	
	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	req1 = requests.get(url, headers={'Content-Type': 'application/json'})
        
	
	#Getting the uuid of a Item
	item_name=title
	for i in req1.json():
		if (item_name == i['name']):
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
	
	response = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if response.status_code==200:
		return 1
	else: 
		return 0


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

