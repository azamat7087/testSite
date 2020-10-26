from django.contrib import admin
from .models import *

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ['phone_number']
admin.site.register(Users, UsersAdmin)
