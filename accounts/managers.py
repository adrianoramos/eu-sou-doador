#!-*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext as _
from django.utils.timezone import utc


class UserManager(BaseUserManager):

    def _create_user(self, name, email, password, is_staff, is_superuser, is_active):
        if not email:
            raise ValueError(_(u'usuários devem ter um endereço de e-mail'))

        now = datetime.utcnow().replace(tzinfo=utc)
        email = self.normalize_email(email)

        user = self.model(
            name=name, email=email,
            is_staff=is_staff, is_superuser=is_superuser, is_active=is_active,
            last_login=now
        )

        user.set_password(password)
        user.save(self._db)

        return user

    def create_user(self, name, email, password):
        return self._create_user(
            name=name, email=email, password=password,
            is_staff=True, is_superuser=False, is_active=True
        )

    def create_superuser(self, name, email, password):
        return self._create_user(
            name=name, email=email, password=password,
            is_staff=True, is_superuser=True, is_active=True
        )
