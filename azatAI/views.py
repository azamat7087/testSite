from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import sys

from .backends import PhoneModelBackend
from .models import *
from .forms import *
from .serializers import *

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class LogUser(View):

    def post(self, request):
        bound_form = LogForm(request.POST)

        if bound_form.is_valid():
            user = PhoneModelBackend.authenticate(phone_number=bound_form.data['phone_number'])
            
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
        return redirect("test_url")

    def get(self, request):
        form = LogForm()
        return render(request, 'azatAI/Login.html', context={'form': form})


class Test(View):
    def get(self, request):
        users = Users.objects.filter(is_active=True)
        return render(request, 'azatAI/test.html', context={'users': users, 'request': request})


class CreateUser(View):
    def post(self, request):
        bound_form = UserForm(request.POST)

        if bound_form.is_valid():

            bound_form.save()

            return redirect('test_url')

        return render(request, 'azatAI/testForm.html', context={'form': bound_form})

    def get(self, request):
        form = UserForm()
        return render(request, 'azatAI/testForm.html', context={'form': form})


class UsersView(APIView):
    def get(self, request, ver):
        users = Users.objects.filter(is_active=True)
        user_ver = 'UsersSerializer_' + ver
        user_ver = str_to_class(user_ver)
        serializer = user_ver(users, many=True)

        return Response(serializer.data)


class DeviceView(APIView):
    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceSer(devices, many=True)

        return Response(serializer.data)


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)