#!-*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from locations.forms import LatLongField

from .models import Donation


class DonationForm(forms.ModelForm):

    position = LatLongField(label=_(u'Posição geográfica'), help_text=_(
        u'Cidade onde está localizado o centro de doação.'), required=True)

    class Meta:
        model = Donation
        fields = ['receiver_name', 'receiver_blood_type', 'receiver_age',
                  'expiration_date', 'donation_center', 'location', 'position', 'reason']

    def clean_receiver_name(self):
        receiver_name = self.cleaned_data.get('receiver_name').strip()
        return receiver_name
