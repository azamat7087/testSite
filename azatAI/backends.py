from django.contrib.auth.backends import ModelBackend
from .models import Users


class PhoneModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None):

        kwargs = {'phone': username}

        try:
            user = Users.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return Users.objects.get(pk=username)
        except Users.DoesNotExist:
            return None