#!-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'hemocentros/$', 'bloodcenters.views.bloodcenters_list',
                           name='bloodcenters_list'),
                       url(r'hemocentros/estado/(?P<state>[\w\W]+)/$',
                           'bloodcenters.views.bloodcenters_by_state', name='bloodcenters_by_state'),
                       url(r'hemocentros/(?P<slug>[-_\w]+)/$',
                           'bloodcenters.views.bloodcenter_detail', name='bloodcenter_detail'),
                       )
