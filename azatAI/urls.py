from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", Main.as_view(), name="main_url"),
    path("reg/1", CreateUser.as_view(), name="create_user_form_url"),
    path("reg/2", CreateUser_OBJ.as_view(), name="create_user_OBJ_form_url"),
    path("users-api/<str:ver>/", UsersView.as_view(), name="user_view_url"),
    path("device-api/", DeviceView.as_view(), name="device-view-url"),
    path("logout/", Logout.as_view(), name="logout_url"),
    path("login/", Login.as_view(), name="log_user_url"),
    path("login/obj", Login_OBJ.as_view(), name="log_user_obj_url"),

]
