from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import User

def home(request):
	request.session.save()
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
	oauth_verifier, email = request.POST['code'], request.POST['email']
	# I want to identify the right session, to get the right token and secret
	# here I take the last object that satisfies the query.
	# It works because they re in creation order

	length = len(User.objects.filter(session_key=session_key))
	user = User.objects.filter(session_key=session_key)[length-1]
	user_biss = User.objects.filter(email=email)
	user_bis = user_biss[len(user_biss)-1]
	if user_bis:
		user = user_bis
	user.discogs_init(email=email,token=user.token, 
						secret=user.secret, oauth_verifier=oauth_verifier)
	user.scrapp_user()
	user.get_collection()
	user.scrapp_collection()

	return render(request, 'login.html', {'code':oauth_verifier}) 
