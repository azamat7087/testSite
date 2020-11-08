from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate, logout
import sys

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RegistrationMixin:

    obj_form = None
    obj = None
    url = None
    template = None

    def post(self, request):
        bound_form = self.obj_form(self.request.POST)

        if bound_form.is_valid():
            if str(self.obj) == 'phone_number':
                bound_form.save()

            elif str(self.obj) == 'id':
                print("RTW")
                k_def = bound_form.save(commit=False)
                rp = get_time_pass()
                k_def.set_password(rp)
                k_def.save()

            obj_cleaned = bound_form.cleaned_data.get(f'{self.obj}')
            raw_password = bound_form.cleaned_data.get('password1')
            if str(self.obj) == 'phone_number':
                user = Users.objects.get(phone_number=obj_cleaned)
                account = authenticate(id=user.id, password=raw_password)

                login(request, account)
                ip = get_client_ip(request)
                os = str(self.request.user_agent.os.family) + " " + str(self.request.user_agent.os.version_string)

                user = Users.objects.get(id__iexact=self.request.user.id)

                Device.objects.create(ip=ip, device_os=os, user=user)

                request.session.set_expiry(2592000)
            elif str(self.obj) == 'id':
                account = authenticate(id=obj_cleaned, password=rp,)

                login(request, account)
                request.session.set_expiry(9999999) # Need we this for objects?



            return redirect('main_url')

        return render(request, self.template, context={'form': bound_form, 'url': self.url})

    def get(self, request):
        form = self.obj_form
        return render(request, self.template, context={'form': form, 'url': self.url})

