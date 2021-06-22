from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.first_name

class Discussion(models.Model):
    text = models.TextField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.createdAt

class Tags(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True,default='Wellness')
    user = models.ManyToManyField(CustomUser,null=True, blank=True,)
    discussion = models.ManyToManyField(Discussion,null=True, blank=True,)
    def __str__(self):
        return self.name