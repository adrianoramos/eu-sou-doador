#!-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'preciso-de-doacao-de-sangue/$',
                           'donations.views.donation_request', name='donation_request'),
                       url(r'precisa-se-de-doadores-de-sangue/(?P<donation_id>\d+)/$',
                           'donations.views.donation_details', name='donation_details'),
                       url(r'pacientes-aguardando-por-doacao-de-sangue/$',
                           'donations.views.donations_list', name='donations_list'),
                       url(r'meus-pedidos/$', 'donations.views.donations_list_by_user',
                           name='donations_list_by_user'),
                       url(r'meus-pedidos/atualizar/(?P<donation_id>\d+)/$',
                           'donations.views.donation_request_update', name='donation_request_update'),
                       )
