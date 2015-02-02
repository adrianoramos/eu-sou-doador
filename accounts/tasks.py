from __future__ import absolute_import

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from celery import shared_task


@shared_task
def send_signup_mail(name, email):
    email_subject = _(u'Bem-vindo(a) ao Eu Sou Doador, %s!' % name)
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = email
    email_body = render_to_string('accounts/signup_email.txt', {'name': name})

    send_mail(email_subject, email_body, email_from, [email_to])
