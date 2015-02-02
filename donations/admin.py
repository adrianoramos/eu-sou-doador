#!-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from models import Donation


admin.site.register(Donation)
