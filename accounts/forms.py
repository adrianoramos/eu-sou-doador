#!-*- coding: utf-8 -*-
import re

from datetime import datetime
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.contrib.gis import forms

from locations.forms import LatLongField

from .models import User, UserProfile


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        return email

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        label=(_(u"Password")),
        help_text= _(u"Raw passwords are not stored, so there is no way to see "
                     "this user's password, but you can change the password "
                     "using <a href=\"password/\">this form</a>.")
    )

    class Meta:
        model = User

    def clean_password(self):
        return self.initial["password"]


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name']


class UserProfileForm(forms.ModelForm):

    position = LatLongField(label=_(u'Posição geográfica'), help_text=_(
        u'Informe de maneira mais detalhada sua localização.'), required=True)

    class Meta:
        model = UserProfile
        fields = ['gender', 'birth_date', 'blood_type',
                  'location', 'position', 'mobile_phone']

    def clean_mobile_phone(self):
        mobile_phone = (lambda x: x if x.isdigit() else re.sub('[( )]', '', x))(
            self.cleaned_data.get('mobile_phone').strip())
        return mobile_phone
