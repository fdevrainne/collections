from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
	return render(request, 'home.html')

def login(request):
	code = request.POST['code']
	return render(request, 'login.html', {'code':code}) 
