from django.db import models
from StudentSublease_Backend import constants
from utils.models import Address
from users.models import SubleaseUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import time
from PIL import Image
import os


class Amenity(models.Model):
    amenity_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.amenity_name

    # This method should only be run once through the shell, to populate list of amenities in the database
    @classmethod
    def populate_amenities(cls):
        supported_amenities = constants.SUPPORTED_AMENITIES
        for amenity in supported_amenities:
            to_add = Amenity(amenity)
            to_add.save()


class StudentListing(models.Model):

    class GenderPreferences(models.IntegerChoices):
        NO_PREFERENCE = 0
        MALE_ONLY = 1
        FEMALE_ONLY = 2
    # Basic Information
    title = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=False)
    lister = models.ForeignKey(SubleaseUser, on_delete=models.CASCADE)
    listed_date = models.DateTimeField(default=timezone.now)

    # Apartment unit details
    description = models.TextField(blank=True, null=True)
    num_bed = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Number of beds in the whole unit", null=False)
    num_bath = models.FloatField(verbose_name="Number of baths in the whole unit", null=False, validators=[MinValueValidator(0)])
    amenities = models.ManyToManyField(Amenity, blank=True)
    gender_preference = models.IntegerField(verbose_name='gender preference',
        choices=GenderPreferences.choices,
        default=GenderPreferences.NO_PREFERENCE)

    # Sublease details
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    rent_per_month = models.FloatField(null=False, validators=[MinValueValidator(0)])

    num_tenants = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Number of tenants", null=False)
    fees = models.FloatField(verbose_name="Applicable fees on the sublease", default=0, validators=[MinValueValidator(0)])

    def json_representation(self):
        amenities_val = self.amenities.all()
        amenities = list()
        for amenity in amenities_val:
            amenities.append(amenity.amenity_name)
        return {
            'pk' : self.pk,
            'title' : self.title,
            'address' : str(self.address),
            'lister' : self.lister.json_representation(),
            'listed_date' : self.listed_date,
            'description' : self.description,
            'num_bed' : self.num_bed,
            'num_bath' : self.num_bath,
            'amenities' : amenities,
            'gender_preference' : self.gender_preference,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
            'rent_per_month' : self.rent_per_month,
            'num_tenants' : self.num_tenants,
            'fees' : self.fees
        }


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    millis = int(round(time.time() * 1000))
    filename = str(instance.listing.id) + "-" + str(millis) + "." + ext
    return os.path.join('listing_pics/' , filename)


class StudentListingImages(models.Model):
    listing = models.ForeignKey(StudentListing, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to=get_file_path, null=False)

    def __str__(self):
        return "Image for {title}".format(title=self.listing.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image)
            if img.height > constants.MAX_LISTING_IMAGE_SIZE_HEIGHT or img.width > constants.MAX_LISTING_IMAGE_SIZE_WIDTH:
                output_size = (constants.MAX_LISTING_IMAGE_SIZE_WIDTH,
                            constants.MAX_LISTING_IMAGE_SIZE_HEIGHT)
                img.thumbnail(output_size)
                try:
                    img.save(self.image.path)
                except NotImplementedError:
                    pass
