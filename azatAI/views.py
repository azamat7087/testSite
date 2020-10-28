from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
import random
# Create your views here.
used_hex_id = []

class Test(View):
    def get(self, request):
        users = Users.objects.all()
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

