#!-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'login/$', 'django.contrib.auth.views.login',
       {'template_name': 'accounts/login.html'}, name='login'),
   url(r'logout/$', 'django.contrib.auth.views.logout',
       {'next_page': '/'}, name='logout'),
   url(r'quero-doar-sangue/$',
       'accounts.views.signup', name='signup'),
   url(r'eu-sou-doador-de-sangue/$',
       'accounts.views.signup_done', name='signup_done'),
   url(r'perfil/atualizar/$', 'accounts.views.profile_update',
       name='profile_update'),
   url(r'senha/alterar/$', 'django.contrib.auth.views.password_change',
       {'template_name': 'accounts/password_change.html'}, name='password_change'),
   url(r'senha/alterar/finalizado/$', 'django.contrib.auth.views.password_change_done',
       {'template_name': 'accounts/password_change_done.html'}, name='password_change_done'),
   url(r'senha/redefinir/$', 'django.contrib.auth.views.password_reset',
       {'template_name': 'accounts/password_reset.html', 'subject_template_name': 'accounts/password_reset_subject.txt', 'email_template_name': 'accounts/password_reset_email.html'}, name='password_reset'),
   url(r'senha/redefinir/finalizado/$', 'django.contrib.auth.views.password_reset_done',
       {'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
   url(r'senha/redefinir/confirmar/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {
       'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
   url(r'senha/redefinir/completo/$', 'django.contrib.auth.views.password_reset_complete',
       {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
)
