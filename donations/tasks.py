from __future__ import absolute_import

from operator import or_

from django.conf import settings
from django.contrib.gis.measure import D
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from celery import shared_task

from accounts.models import UserProfile
from donations.models import Donation


@shared_task
def send_mail_compatible_donors(donation_id):
    donation = Donation.objects.get(pk=donation_id)
    compatible_blood_types = donation.get_compatible_blood_types()
    compatible_donors = UserProfile.objects.filter(position__distance_lte=(donation.position, D(m=100000))).distance(
        donation.position).filter(reduce(or_, [Q(blood_type=b) for b, d in compatible_blood_types]))

    email_subject = _(u'Precisa-se de doadores %s em %s' %
                      (donation.get_compatible_blood_types_formatted(), donation.location))
    email_from = settings.DEFAULT_FROM_EMAIL
    email_body = render_to_string('donations/donation_request_email.txt', {'donation_id': donation.id, 'receiver_name': donation.receiver_name, 'compatible_blood_types': donation.get_compatible_blood_types_formatted(
    ), 'expiration_date': donation.expiration_date, 'donation_center': donation.donation_center, 'location': donation.location})
    email_messages = ()

    for donor in compatible_donors:
        email_messages += ((email_subject, email_body,
                            email_from, [donor.user.email]),)

    send_mass_mail(email_messages)
