from django.core.management.base import BaseCommand

from sublease.models import Amenity
from users.models import SubleaseUser
from utils.models import College
import os
class Command(BaseCommand):

    def handle(self, *args, **options):
        College.populate_college_data("utils/all_college_data.json")
        Amenity.populate_amenities()
        self.stdout.write(self.style.SUCCESS('Successfully loaded the database with options.'))

        if not SubleaseUser.objects.filter(email="teamcoders@gmail.com").exists():
            password = "teamcoders123"
            SubleaseUser.objects.create_superuser("teamcoders@gmail.com", "Admin", "Admin", "Georgia Institute of Technology", password=password)
