from django.contrib import admin
from .models import *

# Register your models here.


class UsersAdmin(admin.ModelAdmin):

    list_display = ['phone_number']
    exclude = ['id', 'update_date', 'session_expire','registration_date', 'is_active']



admin.site.register(Users, UsersAdmin)
