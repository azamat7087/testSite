from django.contrib import admin
from .models import *

# Register your models here.


class UsersAdmin(admin.ModelAdmin):

    list_display = ['phone_number']
    exclude = ['id']



admin.site.register(Users, UsersAdmin)
