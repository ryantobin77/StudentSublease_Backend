import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.http import HttpResponse
from sublease.models import Amenity, StudentListing, StudentListingImages
from utils.models import Address
from users.models import SubleaseUser
from datetime import datetime
from utils import utilities
from StudentSublease_Backend import constants


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
        amenities = get_amenities(request=request)
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
        new_listing = StudentListing.objects.create(title=request.POST['title'], address=address, lister=lister, description=request.POST['description'], num_bed=request.POST['num_bed'], num_bath=request.POST['num_bath'], 
                            gender_preference=request.POST['gender_preference'], start_date=start_date, end_date=end_date, rent_per_month=request.POST['rent_per_month'], num_tenants=request.POST['num_tenants'], fees=request.POST['fees'])
        new_listing.amenities.set(amenities)
        for image in request.FILES.getlist("file"):
            StudentListingImages.objects.create(listing=new_listing, image=image)
        new_listing.save()
        json_response_listing = new_listing.json_representation()
        json_response_listing["distance"] = 0.0
        return JsonResponse(json_response_listing, status=201)
    else:
        return HttpResponse(status=400)


def get_amenities(request):
    amenities = Amenity.objects.none()
    if 'amenity_1' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_1'])
    if 'amenity_2' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_2'])
    if 'amenity_3' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_3'])
    if 'amenity_4' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_4'])
    if 'amenity_5' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_5'])
    if 'amenity_6' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_6'])
    if 'amenity_7' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_7'])
    if 'amenity_8' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_8'])
    if 'amenity_9' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_9'])
    if 'amenity_10' in request.POST:
        amenities |= Amenity.objects.filter(amenity_name=request.POST['amenity_10'])
    return amenities


@csrf_exempt
def search_listings(request):
    filtered_listings = []
    if request.method == "GET" and 'lat' in request.GET and 'long' in request.GET:
        listings = StudentListing.objects.all().order_by('-listed_date')
        for listing in listings:
            lat1 = float(request.GET['lat'])
            long1 = float(request.GET['long'])
            distance = utilities.find_distance(lat1=lat1, long1=long1, lat2=listing.address.lat, long2=listing.address.long)
            if distance <= constants.DEFAULT_DISTANCE_BETWEEN_LOCATIONS:
                listing_result = listing.json_representation()
                listing_result["distance"] = round(distance, 2)
                filtered_listings.append(listing_result)
        return JsonResponse(filtered_listings, safe=False, status="200")
    else:
        return JsonResponse(filtered_listings, safe=False, status="400")


@csrf_exempt
def delete_listing(request):
    if request.method == "POST" and 'lister_pk' in request.POST and 'listing_pk' in request.POST:
        lister_pk = request.POST['lister_pk']
        listing_pk = request.POST['listing_pk']
        try:
            lister = SubleaseUser.objects.get(pk=lister_pk)
            listing = StudentListing.objects.get(pk=listing_pk)
        except:
            return HttpResponse(status=400)
        if lister.pk == listing.lister.pk:
            listing.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def my_listings(request):
    if request.method == "POST" and 'lister_pk' in request.POST:
        lister_pk = request.POST['lister_pk']
        try:
            lister = SubleaseUser.objects.get(pk=lister_pk)
        except SubleaseUser.DoesNotExist:
            return HttpResponse(status=400)
        listings = StudentListing.objects.filter(lister=lister).order_by('-listed_date')
        results = [listing.json_representation() for listing in listings]
        return JsonResponse(results, safe=False, status="200")
    else:
        return HttpResponse(status=400)


 