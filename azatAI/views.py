import platform
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import sys
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from .serializers import *
import re
from .utils import *
'''Functions'''

def get_time_pass():
    time_pass = str(datetime.now())[14:16]
    time_pass += str(int(time_pass) + 1) + time_pass
    if len(time_pass) < 6:
        time_pass1 = ""
        for i in range(len(time_pass)):
            time_pass1 += time_pass[i]
            if i == 1:
                time_pass1 += "0"
        time_pass = time_pass1
    return time_pass

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
        if request.user.is_authenticated and request.user.is_admin == False and request.user.phone_number:
            device = Device.objects.get(user=request.user.id)
            os = str(request.user_agent.os.family) + " " + request.user_agent.os.version_string
            browser = str(request.user_agent.browser.family) + " " + request.user_agent.browser.version_string
            device_id = device.device_id
            obb = Users.objects.get(id__iexact='ffad5457')
            ip = get_client_ip(request)
            head = get_header(request)
            return render(request, 'azatAI/Main.html', context={'users': users,
                                                                'request': request,
                                                                'os': os,
                                                                'header': head,
                                                                'ip': ip,
                                                                'device_id': device_id,
                                                                'browser': browser,
                                                                'obb': obb,
                                                                })
        else:
            return render(request, 'azatAI/Main.html', context={'users': users,
                                                                'request': request})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('main_url')


class Login(View):
    def post(self, request):
        bound_form = LogForm(request.POST)

        if bound_form.is_valid():
            phone_number = request.POST['phone_number']
            password = request.POST['password']
            user = authenticate(phone_number=phone_number, password=password)

            if user:
                login(request, user)
                user = Users.objects.get(phone_number=request.user.phone_number)
                user.last_update = datetime.now()
                user.last_login = datetime.now()
                user.save()

                request.session.set_expiry(2592000)
                return redirect('main_url')

            return redirect('main_url')

        return render(request, 'azatAI/Login.html', context={'form': bound_form})

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('main_url')

        form = LogForm
        return render(request, 'azatAI/Login.html', context={'form': form})

class Login_OBJ(View):
    def post(self, request):
        bound_form = LogForm_OBJ(request.POST)

        if bound_form.is_valid():
            id = request.POST['id']
            password = request.POST['password']
            user = authenticate(id=id, password=password)

            if user:
                login(request, user)
                user = Users.objects.get(id=request.user.id)
                user.last_update = datetime.now()
                user.last_login = datetime.now()
                user.save()

                request.session.set_expiry(2592000)
                return redirect('main_url')

            return redirect('main_url')

        return render(request, 'azatAI/Login_OBJ.html', context={'form': bound_form})

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('main_url')

        form = LogForm_OBJ
        return render(request, 'azatAI/Login_OBJ.html', context={'form': form})


class CreateUser(RegistrationMixin, View):
    obj_form = RegistrationForm
    obj = 'phone_number'
    url = 'create_user_form_url'
    template = 'azatAI/registration.html'

class CreateUser_OBJ(RegistrationMixin, View):
    obj_form = RegistrationForm_OBJ
    obj = 'id'
    url = 'create_user_OBJ_form_url'
    template = 'azatAI/registration_obj.html'

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

