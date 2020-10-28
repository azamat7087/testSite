from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import random
# Create your models here.

def get_hex_id():
    id = random.randint(1, 4294967295)
    hex_id = str(hex(id))[2:]
    return hex_id


class Users(models.Model):

    id = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    phone_number = PhoneNumberField(unique=True, blank=False)

    def __str__(self):
        return str(self.phone_number)

    def save(self, *args, **kwargs):
        while(True):
            id = get_hex_id()
            ids = Users.objects.all()
            used_hex_id = []

            for i in ids:
                used_hex_id.append(i.id)

            if id not in used_hex_id:
                self.id = id
                break

            if len(used_hex_id) > 4294967295:
                raise FullMemoryException
                break



        super(Users, self).save(*args, **kwargs)


class FullMemoryException(Exception):
    pass