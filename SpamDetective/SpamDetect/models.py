from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CutomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone Number Must Be set")
        user = self.model(phone_number = phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = CutomUserManager()

    def __str__(self):
        return self.phone_number
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)

    

    def __str__(self):
        return self.name

class Spam(models.Model):
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.number
    


    
   


