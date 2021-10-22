import os
import time

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image
from StudentSublease_Backend import constants
from utils.models import College, CollegeDomain


class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_sublease_user(self, email, first_name, last_name, college, is_confirmed=False, password=None, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        if not college:
            raise ValueError('Users must have a college')

        college_object = College.objects.get(pk=college)

        if not is_superuser and not SubleaseUser.has_valid_email_ending(email=email, college=college_object):
            raise ValueError("This user must register with a {college_name} email address".format(college_name=college_object.college_name))

        sublease_user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            college=college_object,
            is_confirmed=is_confirmed,
        )
        sublease_user.set_password(password)
        sublease_user.save()
        return sublease_user

    def create_superuser(self, email, first_name, last_name, college, password=None):
        sublease_user = self.create_sublease_user(email, first_name, last_name, college, password=password, is_superuser=True)
        sublease_user.is_admin = True
        sublease_user.is_confirmed = True
        sublease_user.set_password(password)
        sublease_user.save()
        return sublease_user


class SubleaseUser(AbstractBaseUser):

    username = None
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=10, null=True, blank=True, unique=True, validators=[RegexValidator(
            regex='^[0-9]*$',
            message='The phone number must only contain numbers in the format 01234567890',
            code='invalid_phone_number'
        )])
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    college = models.ForeignKey(College, on_delete=models.PROTECT, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False) # For if a user has been reported too many times

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'college',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @classmethod
    def has_valid_email_ending(cls, email, college):
        if email is None:
            return False
        elif college is None:
            raise False
        else:
            college_domains = CollegeDomain.objects.filter(college=college)
            for college_domain in college_domains:
                index = len(email) - len(college_domain.domain)
                email_ending = email[index:]
                if email_ending == college_domain.domain:
                    return True
            return False

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    millis = int(round(time.time() * 1000))
    filename = str(instance.user.id) + "-" + str(millis) + "." + ext
    return os.path.join('profile_pics/' , filename)

class Profile(models.Model):
    user = models.OneToOneField(SubleaseUser, on_delete=models.CASCADE, null=False, primary_key=True)
    image = models.ImageField(upload_to=get_file_path, null=False)

    def __str__(self):
        return "Profile for {email}".format(email=self.user.email)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image)
            if img.height > constants.MAX_PROFILE_IMAGE_SIZE or img.width > constants.MAX_PROFILE_IMAGE_SIZE:
                output_size = (constants.MAX_PROFILE_IMAGE_SIZE, constants.MAX_PROFILE_IMAGE_SIZE)
                img.thumbnail(output_size)
                try:
                    img.save(self.image.path)
                except NotImplementedError:
                    pass
