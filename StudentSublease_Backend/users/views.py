import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.http import HttpResponse
from sublease.models import Amenity, StudentListing
from utils.models import Address
from users.models import SubleaseUser
from users.models import UserManager 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.


@csrf_exempt
def signup(request):
	if (request.method == "POST" and 'email' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST and 'password' in request.POST and 'college' in request.POST):
		
		email = request.POST['email']
		fname = request.POST['first_name']
		lname = request.POST['last_name']
		college = request.POST['college']
		password = request.POST['password']

		myuser = SubleaseUser.objects.create_sublease_user(email = email, first_name = fname, last_name = lname, college = college, password = password)

		myuser.save()

		return JsonResponse(myuser.json_representation(), status = 201)

	else: 

		return HttpResponse(status = 400)


@csrf_exempt
def login(request):
	if (request.method == "POST"):
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(email = email, password = password)

		if user is not None:
			auth_login(request, user)
			return HttpResponse(status = 201)
		else:
			return HttpResponse(status = 400)

@csrf_exempt
def logout(request):

	auth_logout(request)
	return HttpResponse(status = 201)

