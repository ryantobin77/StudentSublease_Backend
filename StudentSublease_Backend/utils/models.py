import datetime
import json
import os
import time
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=2, null=False, validators=[RegexValidator(
        r'^((A[LKZR])|(C[AOT])|(D[EC])|(FL)|(GA)|(HI)|(I[DLNA])|(K[SY])|(LA)|(M[EDAINSOT])|(N[EVHJMYCD])|(O[HKR])|(PA)|(RI)|(S[CD])|(T[NX])|(UT)|(V[TA])|(W[AVIY]))$')])
    zip = models.CharField(max_length=5, null=False, validators=[
                           RegexValidator(r'^[0-9]{5}$')])
    lat = models.FloatField(null=False)
    long = models.FloatField(null=False)
    country = models.CharField(max_length=100, null=False)

    def __str__(self):
        return str(self.street) + ", " + str(self.city) + ", " + str(self.state) + " " + str(self.zip)

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    millis = int(round(time.time() * 1000))
    filename = instance.college_name.strip() + "-image-" + str(millis) + "." + ext
    return os.path.join('college_images/' , filename)

class College(models.Model):
    college_name = models.CharField(max_length=100, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=False)
    image = models.ImageField(upload_to=get_file_path, null=True)

    @classmethod
    def populate_college_data(cls, file):
        data = None
        with open(file, "r", encoding='utf-8') as fin:
            data = json.load(fin)
        if data is None:
            raise AttributeError("university data file not found")

        colleges = []
        for university in data:
            if university["country"] != "United States":
                continue
            name = university["name"]
            country = ""
            state = ""
            city = ""
            address = ""
            zip_code = ""
            coordinates = []
            domain = university["domains"][0]
            if "coordinates" in university:
                coordinates = university["coordinates"]
            if "address_info_from_api" in university:
                if "country" in university["address_info_from_api"]:
                    country = university["address_info_from_api"]["country"]
                if "state" in university["address_info_from_api"]:
                    state = university["address_info_from_api"]["state"]
                if "city" in university["address_info_from_api"]:
                    city = university["address_info_from_api"]["city"]
                if "address" in university["address_info_from_api"]:
                    address = university["address_info_from_api"]["address"]
                if "zip_code" in university["address_info_from_api"]:
                    zip_code = university["address_info_from_api"]["zip_code"]

            if city != "" and country != "" and zip_code != "" and address != "" and len(coordinates) == 2 and len(state) == 2:
                colleges.append((name, address, city, state, country, domain))
                address = Address(street=address, city=city, state=state, zip=zip_code, lat=coordinates[1], long=coordinates[0], country="United States of America")
                address.save()
                college = College(college_name=name, address=address)
                college.save()
                domain = CollegeDomain(domain=domain, college=college)
                domain.save()

        print(str(len(colleges)) + " colleges added.")

    def __str__(self):
        return self.college_name

class CollegeDomain(models.Model):
    domain = models.CharField(max_length=100, primary_key=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return "{domain} for {college}".format(college=self.college.college_name, domain=self.domain)

class ClosestCollege(models.Model):
    college = models.ForeignKey(College, on_delete=models.PROTECT)
    listing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    distance = models.FloatField(null=False, default=0)

    def __str__(self):
        return "{address} for {college}".format(college=self.college.college_name, address=self.listing_address.street)
