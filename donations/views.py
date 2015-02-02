#!-*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from accounts.forms import UserForm
from accounts.models import User
from accounts.tasks import send_signup_mail

from .models import Donation
from .forms import DonationForm
from .tasks import send_mail_compatible_donors


def donation_request(request):
    donation_form = DonationForm(data=request.POST or None)
    user_form = UserForm(data=request.POST or None)

    if donation_form.is_valid():
        donation = donation_form.save(commit=False)
        user = None
        send_mail_new_user = False

        if request.user.is_authenticated():
            user = request.user
        elif user_form.is_valid():
            user = user_form.save()
            send_mail_new_user = True

        if user:
            donation.user = user
            donation.save()
            send_mail_compatible_donors.delay(donation.id)

            if send_mail_new_user:
                send_signup_mail.delay(user.name, user.email)

            messages.add_message(request, messages.SUCCESS, _(
                u'Sua solicitação foi gravada com sucesso! Vamos procurar doadores compatíveis com o tipo sanguíneo informado. Você pode ajudar compartilhando este link com amigos através das redes sociais.'))
            return redirect('donation_details', donation_id=donation.id)

    return render_to_response('donations/donation_request.html', {
        'donation_form': donation_form,
        'user_form': user_form
    }, context_instance=RequestContext(request))


def donations_list(request):
    donations = Donation.objects.filter(expiration_date__gte=datetime.utcnow(
    ).date()).order_by('expiration_date', '-modified')
    return render_to_response('donations/donations_list.html', {
        'donations': donations
    }, context_instance=RequestContext(request))


def donation_details(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)
    return render_to_response('donations/donation_details.html', context_instance=RequestContext(request, {'donation': donation}))


@login_required()
def donations_list_by_user(request):
    donations = Donation.objects.filter(user=request.user)
    return render_to_response('donations/donations_list_by_user.html', {
        'donations': donations
    }, context_instance=RequestContext(request))


@login_required
def donation_request_update(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id, user=request.user)
    donation_form = DonationForm(data=request.POST or None, instance=donation)

    if donation_form.is_valid():
        donation_form.save()
        messages.add_message(request, messages.SUCCESS, _(
            u'Obrigado, as informações do pedido foram atualizadas.'))
        return redirect('donations_list_by_user')

    return render_to_response('donations/donation_request_update.html', {
        'donation_form': donation_form
    }, context_instance=RequestContext(request))
