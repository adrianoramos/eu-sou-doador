#!-*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _

class LatLongWidget(forms.MultiWidget):
    """
    A Widget that splits Point input into two latitude/longitude boxes.
    """

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (forms.TextInput(attrs=attrs),
                   forms.TextInput(attrs=attrs))
        super(LatLongWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return tuple(reversed(value.coords))
        return (None, None)

class LatLongField(forms.MultiValueField):

    widget = LatLongWidget
    srid = 4326

    default_error_messages = {
        'invalid_latitude' : _(u'Informe uma latitude válida.'),
        'invalid_longitude' : _(u'Informe uma longitude válida.'),
    }

    def __init__(self, *args, **kwargs):
        fields = (forms.FloatField(min_value=-90, max_value=90),
                  forms.FloatField(min_value=-180, max_value=180))
        super(LatLongField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if latitude or longitude is empty
            # (possible if LatLongField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_latitude'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_longitude'])
            # SRID=4326;POINT(1.12345789 1.123456789)
            srid_str = 'SRID=%d'%self.srid
            point_str = 'POINT(%f %f)'%tuple(reversed(data_list))
            return ';'.join([srid_str, point_str])
        return None