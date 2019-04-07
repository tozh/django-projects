# from .models import CustomUser
from django.contrib.auth import get_user_model
import logging

mylog = logging.getLogger(__name__)


class PhoneBackend(object):
    def authenticate(self, username=None, password=None):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(phone = username)
            if user.check_password(password):
                return user
            else:
                return None
        except my_user_model.DoesNotExist:
                return None
    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None


class EmailBackend(object):
    def authenticate(self, username=None, password=None):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(email = username)
            if user.check_password(password):
                return user
            else:
                return None
        except my_user_model.DoesNotExist:
                return None

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk = user_id)
        except my_user_model.DoesNotExist:
            return None

# class TokenBackend(object):
#     def authenticate(self, request, token=None):

