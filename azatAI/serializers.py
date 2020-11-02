from rest_framework import serializers
from .models import *


class UsersSerializer_v1(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'phone_number')


class UsersSerializer_v2(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'phone_number', 'registration_date')

class DeviceSer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields =  ("__all__")

class UsersSerializer_v3(serializers.ModelSerializer):
    devices = DeviceSer(many=True)
    class Meta:
        model = Users
        fields = ('__all__')
