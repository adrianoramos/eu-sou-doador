#!-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel
from autoslug import AutoSlugField


class BloodCenter(TimeStampedModel, models.Model):
    name = models.CharField(_(u'nome'), max_length=64)
    email = models.EmailField(
        _(u'e-mail'), max_length=128, null=True, blank=True)
    website = models.URLField(
        _(u'site'), max_length=128, null=True, blank=True)
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('administradores'), blank=True)
    slug = AutoSlugField(populate_from='name', max_length=64,
                         unique=True, always_update=True, db_index=True)

    class Meta:
        verbose_name = _(u'hemocentro')
        verbose_name_plural = _(u'hemocentros')


class Address(TimeStampedModel, models.Model):
    blood_center = models.ForeignKey(BloodCenter, verbose_name=_('hemocentro'))
    zip_code = models.CharField(_(u'cep'), max_length=8)
    street = models.CharField(_(u'logradouro'), max_length=64)
    number = models.CharField(_(u'número'), blank=True, max_length=8)
    neighborhood = models.CharField(_(u'bairro'), blank=True, max_length=64)
    city = models.CharField(_(u'cidade'), max_length=64)
    state = models.CharField(_(u'estado'), max_length=64)
    position = models.PointField(
        verbose_name=_(u'posição'), null=True, blank=False, spatial_index=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = _(u'endereço')
        verbose_name_plural = _(u'endereços')


class Phone(TimeStampedModel):
    blood_center = models.ForeignKey(BloodCenter, verbose_name=_('hemocentro'))
    number = models.CharField(_(u'número'), max_length=16)

    class Meta:
        verbose_name = _(u'telefone')
        verbose_name_plural = _(u'telefones')


class BloodStock(TimeStampedModel, models.Model):
    blood_center = models.ForeignKey(BloodCenter, verbose_name=_('hemocentro'))
    BLOOD_SUPPLY_CHOICES = Choices(
        (0, 'NoStock', _(u'Sem estoque')),
        (1, 'Low', _(u'Baixo')),
        (2, 'Medium', _(u'Médio')),
        (3, 'High', _(u'Alto')),
    )
    o_negative_stock_level = models.SmallIntegerField(
        _(u'O-'), choices=BLOOD_SUPPLY_CHOICES)
    o_positive_stock_level = models.SmallIntegerField(
        _(u'O+'), choices=BLOOD_SUPPLY_CHOICES)
    a_negative_stock_level = models.SmallIntegerField(
        _(u'A-'), choices=BLOOD_SUPPLY_CHOICES)
    a_positive_stock_level = models.SmallIntegerField(
        _(u'A+'), choices=BLOOD_SUPPLY_CHOICES)
    b_negative_stock_level = models.SmallIntegerField(
        _(u'B-'), choices=BLOOD_SUPPLY_CHOICES)
    b_positive_stock_level = models.SmallIntegerField(
        _(u'B+'), choices=BLOOD_SUPPLY_CHOICES)
    ab_negative_stock_level = models.SmallIntegerField(
        _(u'AB-'), choices=BLOOD_SUPPLY_CHOICES)
    ab_positive_stock_level = models.SmallIntegerField(
        _(u'AB+'), choices=BLOOD_SUPPLY_CHOICES)

    class Meta:
        get_latest_by = 'modified'
        verbose_name = _(u'estoque de sangue')
        verbose_name_plural = _(u'estoques de sangue')
