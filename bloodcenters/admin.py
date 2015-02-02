#!-*- coding: utf-8 -*-
from django.contrib.gis import admin
# from django.contrib import admin

from models import BloodCenter, Address, Phone, BloodStock


class AddressInline(admin.StackedInline):
    model = Address
    max_num = 1
    can_delete = False


class PhoneInline(admin.TabularInline):
    model = Phone


class BloodCenterAdmin(admin.ModelAdmin):
    inlines = [AddressInline, PhoneInline]
    list_display = ('name', 'created')
    filter_horizontal = ('admins',)
    list_filter = ()
    ordering = ('-created',)


admin.site.register(Address, admin.OSMGeoAdmin)
admin.site.register(BloodStock)
admin.site.register(BloodCenter, BloodCenterAdmin)
