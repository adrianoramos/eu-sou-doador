#!-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from .sitemap import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^politica-de-privacidade/$', TemplateView.as_view(template_name='terms-and-privacy.html'), name='terms_and_privacy'),
    url(r'^duvidas-sobre-doacao-de-sangue/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^quem-nao-pode-doar-sangue/$', TemplateView.as_view(template_name='who-cant-donate.html'), name='who_cant_donate'),
    url(r'^quem-pode-doar-sangue/$', TemplateView.as_view(template_name='who-can-donate.html'), name='who_can_donate'),

    # Home urls
    url(r'^', include('home.urls')),

    # Accounts urls
    url(r'^', include('accounts.urls')),

    # Donations urls
    url(r'^', include('donations.urls')),

    # Bloodcenter urls
    url(r'^', include('bloodcenters.urls')),

    # Contact form urls
    url(r'^fale-conosco/', include('contact_form.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

sitemaps = {
    'static': StaticViewSitemap,
    'donations': DonationsSitemap,
    'donations_list': DonationsListSitemap,
    'bloodcenters': BloodCentersSitemap,
}

urlpatterns += patterns('',
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
)