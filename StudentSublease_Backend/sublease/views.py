import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.http import HttpResponse
from sublease.models import Amenity, StudentListing
from utils.models import Address
from users.models import SubleaseUser


# Create your views here.
def home(request):
    return HttpResponse("This is the backend for Team Coder's Student Sublease project!")


@csrf_exempt
def create_listing(request):
    if (request.method == "POST" and 'title' in request.POST and 'street' in request.POST and 'city' in request.POST and 'state' in request.POST and 
        'zip' in request.POST and 'lat' in request.POST and 'long' in request.POST and 'lister_pk' in request.POST and 'description' in request.POST and 
        'num_bed' in request.POST and 'num_bath' in request.POST and 'gender_preference' in request.POST and 
        'start_date' in request.POST and 'end_date' in request.POST and 'rent_per_month' in request.POST and 'fees' in request.POST and 
        'num_tenants' in request.POST):
        try:
            lister = SubleaseUser.objects.get(pk=request.POST['lister_pk'])
        except SubleaseUser.DoesNotExist:
            return HttpResponse(status=400)
        
        address = Address.objects.create(street=request.POST['street'], city=request.POST['city'], state=request.POST['state'], zip=request.POST['zip'], lat=request.POST['lat'], long=request.POST['long'], country="United States of America")
        amenities = Amenity.objects.all()
        new_listing = StudentListing.objects.create(title=request.POST['title'], address=address, lister=lister, description=request.POST['description'], num_bed=request.POST['num_bed'], num_bath=request.POST['num_bath'], 
                            gender_preference=request.POST['gender_preference'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], rent_per_month=request.POST['rent_per_month'], num_tenants=request.POST['num_tenants'], fees=request.POST['fees'])
        new_listing.amenities.set(amenities)
        new_listing.save()
        return JsonResponse(new_listing.json_representation(), status=201)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def search_listings(request):
    if request.method == "GET":
        listings = StudentListing.objects.all().order_by('-listed_date')
        listing_results = [listing.json_representation() for listing in listings]
        return JsonResponse({'listings' : listing_results}, status="200")
    else:
        return HttpResponse(status=400)



