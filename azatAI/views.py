import platform
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import sys
from django.contrib.auth import login, authenticate
from .models import *
from .forms import *
from .serializers import *
import re

'''Functions'''

def get_header(request):
    regex = re.compile('^HTTP_')
    head = dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))
    return head


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


'''Views'''

class Main(View):
    def get(self, request):
        users = Users.objects.filter(is_active=True)
        device = Device.objects.get(user=request.user.id)
        os = request.user_agent.browser.family
        device_id = device.device_id
        ip = get_client_ip(request)
        head = get_header(request)
        return render(request, 'azatAI/Main.html', context={'users': users,
                                                            'request': request,
                                                            'os': os,
                                                            'header': head,
                                                            'ip': ip,
                                                            'device_id': device_id,
                                                            })


class CreateUser(View):
    def post(self, request):
        bound_form = RegistrationForm(request.POST)

        if bound_form.is_valid():

            bound_form.save()
            phone_number = bound_form.cleaned_data.get('phone_number')
            raw_password = bound_form.cleaned_data.get('password1')
            account = authenticate(phone_number=phone_number, password=raw_password)

            login(request, account)

            head = get_header(request)

            ip = get_client_ip(request)
            os = str(request.user_agent.os.family) + " " + str(request.user_agent.os.version_string)
            user = Users.objects.get(id__iexact=request.user.id)

            Device.objects.create(ip=ip, device_os=os, user=user)

            request.session.set_expiry(2592000)


            return redirect('main_url')

        return render(request, 'azatAI/registration.html', context={'form': bound_form})

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'azatAI/registration.html', context={'form': form})


'''Api Interfaces'''

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

