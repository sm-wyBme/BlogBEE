from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from PIL import Image
from django.conf import settings
import os

#custom UserModel manager
#create a user and create a superuser
class MyAccountManager(BaseUserManager):
    #create a user
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address!")
        if not username:
            raise ValueError("Users must have a username!")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    #create a super user
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username, 
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    profile_image_name = f'profile_images/{self.pk}/{"profile_image.png"}'
    return profile_image_name

def get_default_profile_image_filepath():
    return 'custom_images/dummy-profile.png'


#custom user Model
class Account(AbstractBaseUser):
    #user fields
    email               = models.EmailField(max_length=200, verbose_name='email', unique=True)
    username            = models.CharField(max_length=255, verbose_name='username', unique=True)
    name                = models.CharField(max_length=255, verbose_name='name', null = True, blank=True)
    date_joined         = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin            = models.BooleanField(default=False, verbose_name='is_admin')
    is_staff            = models.BooleanField(default=False, verbose_name='is_staff')
    is_active           = models.BooleanField(default=True) #has to be true
    is_superuser        = models.BooleanField(default=False)
    profile_image       = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image_filepath)
    bio                 = models.TextField(max_length=1000, verbose_name='bio', null=True, blank=True)
    hide_email          = models.BooleanField(default=True)

    objects = MyAccountManager()

    #login using user email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    #has to be overridden
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    #get the file name uploaded by the user and change the name of the file to the generic name
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
