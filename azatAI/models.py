from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Users(models.Model):
    phone_number = PhoneNumberField(unique=True, blank=False)



