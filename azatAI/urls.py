from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", Test.as_view(), name="test_url"),
    path("form/", CreateUser.as_view(), name="create_user_form_url"),
]
