#!-*- coding: utf-8 -*-
from models import User


class AuthEmailBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username.strip().lower())
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
