from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from bloodcenters.models import BloodCenter
from donations.models import Donation

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'login', 'signup', 'bloodcenters_list', 'donation_request', 'terms_and_privacy', 'faq', 'who_cant_donate', 'who_can_donate', 'contact_form']

    def location(self, item):
        return reverse(item)

class DonationsListSitemap(Sitemap):
    priority = 1.0
    changefreq = 'hourly'

    def items(self):
        return ['donations_list']

    def location(self, item):
        return reverse(item)

class DonationsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Donation.objects.all()

    def location(self, item):
        return reverse('donation_details', kwargs={'donation_id': item.id})

    def lastmod(self, obj):
        return obj.modified

class BloodCentersSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return BloodCenter.objects.all()

    def location(self, item):
        return reverse('bloodcenter_detail', kwargs={'slug': item.slug})

    def lastmod(self, obj):
        return obj.modified