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

class Users(models.Model):
    id = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    phone_number = PhoneNumberField(unique=True, blank=False)
    update_date = models.DateField(auto_now=True)
    delete_date = models.DateField(default=get_deadline)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.phone_number)

    # def update_delete_date(self, user):
    #     self.delete_date = user.update_date + timedelta(days=30)
    #     print(datetime.now())
    #     print(self.delete_date)
    #     if datetime.now() > self.delete_date:
    #         self.is_active = False

    def set_id(self, ids):
        while (True):
            id = get_hex_id()

            used_hex_id = []

            for i in ids:
                used_hex_id.append(i.id)
            if id not in used_hex_id:
                self.id = id
                break

            if len(used_hex_id) > 4294967295:
                raise FullMemoryException
                break

    def save(self, *args, **kwargs):
        try:
            user = Users.objects.get(id=self.id)
            self.delete_date = user.update_date + timedelta(days=30)
            print(str(self.delete_date))
            datetime_object = datetime.strptime(str(self.delete_date), '%Y-%m-%d')
            if datetime.now() > datetime_object:
                self.is_active = False

        except Exception:
            pass

        # if not self.id:
        #     try:
        #         ids = Users.objects.all()
        #         self.set_id(self, ids)
        #     except Exception:
        #         pass
        #
        if not self.id:
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


