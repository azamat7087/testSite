from datetime import timedelta, datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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


class UsedID(models.Model):
    used = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.used


class UserManager(BaseUserManager):
    def create_user(self,user_name, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone_number=phone_number,
            user_name=user_name,
            # session_expire=session_expire,
            # last_update=last_update,
            # id=id
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,user_name, phone_number,  password):
        user= self.create_user(
            phone_number=phone_number,
            user_name=user_name,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Users(AbstractBaseUser):
    id = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    user_name = models.CharField(max_length=30,default="")
    phone_number = PhoneNumberField(unique=True, blank=False)
    date_joined = models.DateField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last_login', auto_now=True)
    last_update = models.DateField(auto_now=True)
    session_expire = models.DateField(default=get_deadline)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['user_name']

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(selfs, app_label):
        return True


    def save(self, *args, **kwargs):

        try:
            self.session_expire = self.last_update + timedelta(days=30)
            datetime_object = datetime.strptime(str(self.session_expire), '%Y-%m-%d')
            if datetime.now() > datetime_object:
                if self.is_admin == False:
                    pass
                    # Users.objects.get(phone_number=self.phone_number).delete()

        except Exception:
            pass
        if not self.id:
            self.id = set_id()
        super(Users, self).save(*args, **kwargs)


class FullMemoryException(Exception):
    pass


class Device(models.Model):
    device_id = models.CharField(max_length=8, unique=True, null=False,primary_key=True)
    device_os = models.CharField(max_length=50)
    login_date = models.DateField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE, default="", related_name='devices')

    def __str__(self):
        return self.device_id

    def save(self, *args, **kwargs):
        if not self.device_id:
            self.device_id = set_id()
        super(Device, self).save(*args, **kwargs)

