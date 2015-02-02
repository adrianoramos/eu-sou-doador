#!-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .models import User, UserProfile
from .forms import UserForm, UserProfileForm, UserUpdateForm
from .tasks import send_signup_mail


def signup(request):
    if request.user.is_authenticated():
        messages.add_message(request, messages.WARNING, _(
            u'Você já é um doador cadastrado! Se necessário, verifique e atualize suas informações.'))
        return redirect('profile_update')

    user_form = UserForm(data=request.POST or None)
    user_profile_form = UserProfileForm(data=request.POST or None)

    if user_form.is_valid() and user_profile_form.is_valid():
        user = user_form.save()
        user_profile = user_profile_form.save(commit=False)
        user_profile.user = user
        user_profile.save()

        send_signup_mail.delay(user.name, user.email)

        messages.add_message(request, messages.SUCCESS, _(
            u'Obrigado! Agora você pode receber alertas de pedidos de doação compatíveis com seu tipo sanguíneo e solicitar doação de sangue para um parente ou amigo.'))
        return redirect('signup_done')

    return render_to_response('accounts/signup.html', {
        'user_form': user_form,
        'user_profile_form': user_profile_form
    }, context_instance=RequestContext(request))


def signup_done(request):
    return render_to_response('accounts/signup_done.html', context_instance=RequestContext(request))


@login_required()
def profile_update(request):
    user_form = UserUpdateForm(
        data=request.POST or None, instance=request.user)
    user_profile_form = UserProfileForm(
        data=request.POST or None, instance=request.user.profile)

    if user_form.is_valid() and user_profile_form.is_valid():
        user = user_form.save()
        user_profile = user_profile_form.save(commit=False)
        user_profile.user = user
        user_profile.save()

        messages.add_message(
            request, messages.SUCCESS, _(u'Obrigado, suas informações foram atualizadas.'))
        return redirect('profile_update')

    return render_to_response('accounts/profile_update.html', {'user_form': user_form, 'user_profile_form': user_profile_form}, context_instance=RequestContext(request))
