#!-*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel


def validate_name(name):
    if len(name.split()) < 2:
        raise ValidationError((u'O nome parece não estar completo.'))


def validate_expiration_date(date):
    expiration_date = date
    now_date = datetime.utcnow().date()
    if expiration_date < now_date:
        raise ValidationError((u'Data limite inválida.'))


class Donation(TimeStampedModel, models.Model):
    BLOOD_TYPE_CHOICES = (
        (1, _(u'O-')),
        (2, _(u'O+')),
        (3, _(u'A-')),
        (4, _(u'A+')),
        (5, _(u'B-')),
        (6, _(u'B+')),
        (7, _(u'AB-')),
        (8, _(u'AB+')),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_(u'usuário'))
    receiver_name = models.CharField(
        verbose_name=_(u'nome completo'), max_length=64, validators=[validate_name])
    receiver_blood_type = models.SmallIntegerField(
        verbose_name=_(u'tipo sanguíneo'), choices=BLOOD_TYPE_CHOICES)
    receiver_age = models.SmallIntegerField(verbose_name=_(u'idade'))
    expiration_date = models.DateField(verbose_name=_(u'data limite'), validators=[
                                       validate_expiration_date], help_text=_(u'Data limite para encontrarmos doadores compatíveis.'))
    donation_center = models.CharField(verbose_name=_(u'centro de doação'), max_length=255, help_text=_(
        u'Hospital/unidade onde as pessoas devem ir para doar.'))
    location = models.CharField(
        _(u'localização'), max_length=128, help_text=_(u'Cidade - Estado'))
    position = models.PointField(verbose_name=_(u'posição'), null=True, blank=False, spatial_index=True, help_text=_(
        u'Cidade onde está localizado o centro de doação.'))
    reason = models.TextField(verbose_name=_(u'motivo'), max_length=255, help_text=_(
        u'Descreva o motivo do pedido de doação.'))

    def get_compatible_blood_types(self):
        blood_type = self.receiver_blood_type
        compatible_blood_types = []

        if blood_type == self.BLOOD_TYPE_CHOICES[0][0]:     # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
        elif blood_type == self.BLOOD_TYPE_CHOICES[1][0]:   # O+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[1])    # O+
        elif blood_type == self.BLOOD_TYPE_CHOICES[2][0]:   # A-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[2])    # A-
        elif blood_type == self.BLOOD_TYPE_CHOICES[3][0]:   # A+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[1])    # O+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[2])    # A-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[3])    # A+
        elif blood_type == self.BLOOD_TYPE_CHOICES[4][0]:   # B-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[4])    # B-
        elif blood_type == self.BLOOD_TYPE_CHOICES[5][0]:   # B+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[1])    # O+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[4])    # B-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[5])    # B+
        elif blood_type == self.BLOOD_TYPE_CHOICES[6][0]:   # AB-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[2])    # A-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[4])    # B-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[6])    # AB-
        elif blood_type == self.BLOOD_TYPE_CHOICES[7][0]:   # AB+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[0])    # O-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[1])    # O+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[2])    # A-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[3])    # A+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[4])    # B-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[5])    # B+
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[6])    # AB-
            compatible_blood_types.append(self.BLOOD_TYPE_CHOICES[7])    # AB+
        return compatible_blood_types

    def get_compatible_blood_types_formatted(self):
        blood_types = self.get_compatible_blood_types()
        formmated_list = _(', ').join(unicode(c) for b, c in blood_types)
        return formmated_list

    class Meta:
        verbose_name = _(u'doação')
        verbose_name_plural = _(u'doações')
