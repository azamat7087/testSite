from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import sys

from .models import *
from .forms import *
from .serializers import *


class Test(View):
    def get(self, request):
        users = Users.objects.filter(is_active=True)
        return render(request, 'azatAI/test.html', context={'users': users})

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