#!-*- coding: utf-8 -*-
# from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis import admin

from models import User, UserProfile
from forms import UserChangeForm, UserForm

admin.site.register(User)
admin.site.register(UserProfile, admin.OSMGeoAdmin)
admin.site.unregister(Group)
