from datetime import timedelta, datetime
import time
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import random

# Create your models here.



def get_hex_id():
    id = random.randint(1, 4294967295)
    hex_id = str(hex(id))[2:]
    return hex_id


def get_deadline():
    return datetime.now() + timedelta(days=30)


class UsedID(models.Model):
    used = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.used

def set_id():
    while (True):
        id = get_hex_id()
        ids = UsedID.objects.all()
        used_hex_id = []
        for i in ids:
            used_hex_id.append(i.used)
        if id not in used_hex_id:
            UsedID.objects.create(used=id)
            return id
            break

        if len(used_hex_id) > 4294967295:
            raise FullMemoryException
            break

class Users(models.Model):
    id = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    phone_number = PhoneNumberField(unique=True, blank=False)
    registration_date = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    update_date = models.DateField(auto_now=True)
    session_expire = models.DateField(default=get_deadline)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.phone_number)

    def save(self, *args, **kwargs):

        try:
            self.session_expire = self.update_date + timedelta(days=30)
            datetime_object = datetime.strptime(str(self.session_expire), '%Y-%m-%d')
            if datetime.now() + timedelta(days=35) > datetime_object:
                self.is_active = False

        except Exception:
            pass

        if not self.id:
            self.id = set_id()

        # Device.objects.create(self)
        super(Users, self).save(*args, **kwargs)


class FullMemoryException(Exception):
    pass


class Device(models.Model):
    device_id = models.CharField(max_length=8, unique=True, null=False,primary_key=True)
    device_os = models.CharField(max_length=8)
    login_date = models.DateField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE, default="", related_name='devices')

    def __str__(self):
        return self.device_id

    def save(self, *args, **kwargs):
        self.device_id = set_id()
        self.device_os = set_id()

        super(Device, self).save(*args, **kwargs)