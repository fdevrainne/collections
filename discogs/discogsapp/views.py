from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import User

def home(request):
	request.session.save()
	# The line above is mandatory to populate the session, 
	# or else session_key is None 
	session_key = request.session.session_key

	user = User()
	user.discogs_init()
	url = user.get_url_oauth()

	user.session_key = session_key
	user.save()

	return render(request, 'home.html',{'url':url})

def login(request):
	request.session.save()
	session_key = request.session.session_key

	code = request.POST['code']

	# I want to identify the right session, to get the right token and secret
	length = len(User.objects.filter(session_key=session_key))
	user = User.objects.filter(session_key=session_key)[length-1]
	user.discogs_init(token=user.token, secret=user.secret)
	#user.
	# access token and secret in session
	#discogs_user=DiscogsUser(token=user.token, secret=user.secret)

	user.get_oauth(code)
	user.scrapp_user()
	user.get_collection()
	user.scrapp_collection()

	

	return render(request, 'login.html', {'code':code}) 
