from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
#from django.contrib.auth.models import User as WebsiteUser, auth
from .scrapping.scrapper import DiscogsUser
from .models import User
# Create your views here.

def home(request):
	session_key = request.session.session_key

	# I create a new DBuser, I add session_key, token and secret
	# In login, I access session_key, that allows fo find the DBuser

	# I want to add session_key to the database through the child object DiscogsUser

	#user = User()
	user = DiscogsUser()
	url = user.get_url_oauth()
	user.session_key = session_key
	user.save()

	return render(request, 'home.html',{'url':url})

def login(request):
	session_key = request.session.session_key
	code = request.POST['code']

	# I want to identify the right session, to get the right token and secret
	length = len(User.objects.filter(session_key=session_key))
	user = User.objects.filter(session_key=session_key)[length-1]

	print(user.token)
	print(code)
	print(user.secret)

	# access token and secret in session
	discogs_user=DiscogsUser(token=user.token, secret=user.secret)

	discogs_user.get_oauth(code)
	discogs_user.scrapp_user()
	discogs_user.get_collection()
	discogs_user.scrapp_collection()

	

	return render(request, 'login.html', {'code':code}) 
