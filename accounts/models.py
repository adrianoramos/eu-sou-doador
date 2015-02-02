#!-*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from model_utils import Choices
from model_utils.models import TimeStampedModel

from .managers import UserManager


def validate_name(name):
    if len(name.split()) < 2:
        raise ValidationError((u'O nome parece não estar completo.'))


def validate_birthdate(date):
    birth_date = date
    date_now = datetime.utcnow().date()
    years = (date_now - birth_date).days / 365.2425
    if years < 16:
        raise ValidationError((u'Idade menor que 16 anos.'))
    elif years > 69:
        raise ValidationError((u'Idade maior que 69 anos.'))


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        verbose_name=_(u'nome completo'), max_length=64, validators=[validate_name])
    email = models.EmailField(
        verbose_name=_(u'e-mail'), max_length=128, unique=True, db_index=True)
    is_staff = models.BooleanField(verbose_name=_(u'membro da equipe'), default=False, help_text=_(
        u'Indica que usuário consegue acessar este site de administração.'))
    is_active = models.BooleanField(verbose_name=_(u'ativo'), default=True, help_text=_(
        u'Indica que o usuário será tratado como ativo. Ao invés de excluir contas de usuário, desmarque isso.'))
    date_joined = models.DateTimeField(
        verbose_name=_(u'date joined'),  default=datetime.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_absolute_url(self):
        return '/%s/' % urlquote(self.id)

    def get_full_name(self):
        return self.name.encode('utf-8')

    def get_short_name(self):
        return self.name.split(' ')[0].encode('utf-8')

    def __unicode__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = _(u'usuário')
        verbose_name_plural = _(u'usuários')


class UserProfile(TimeStampedModel, models.Model):
    BLOOD_TYPE_CHOICES = (
        (0, _(u'Não sei meu tipo sanguíneo')),
        (1, _(u'O-')),
        (2, _(u'O+')),
        (3, _(u'A-')),
        (4, _(u'A+')),
        (5, _(u'B-')),
        (6, _(u'B+')),
        (7, _(u'AB-')),
        (8, _(u'AB+'))
    )
    GENDER_CHOICES = (
        (1, _(u'Homem')),
        (2, _(u'Mulher'))
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_(u'usuário'), unique=True)
    gender = models.SmallIntegerField(
        _(u'gênero'), choices=GENDER_CHOICES, null=True)
    blood_type = models.SmallIntegerField(
        _(u'tipo sanguíneo'), choices=BLOOD_TYPE_CHOICES, null=True)
    birth_date = models.DateField(
        _(u'data de nascimento'), null=True, blank=False, validators=[validate_birthdate])
    mobile_phone = models.CharField(_(u'celular'), max_length=16, blank=True)
    location = models.CharField(
        _(u'localização'), max_length=128, help_text=_(u'Bairro, Cidade - Estado'))
    position = models.PointField(verbose_name=_(u'posição'), null=True, blank=False, spatial_index=True, help_text=_(
        u'Informe de maneira mais aproximada possível a sua localização.'))

    objects = models.GeoManager()

    class Meta:
        verbose_name = _(u'perfil de usuário')
        verbose_name_plural = _(u'perfis de usuário')

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
