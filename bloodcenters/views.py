#!-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import BloodCenter, Address


def bloodcenters_list(request):
    bloodcenters = BloodCenter.objects.all().order_by('name')
    states = Address.objects.values('state').distinct().order_by('state')
    return render_to_response('bloodcenters/bloodcenters_list.html', {
        'bloodcenters': bloodcenters,
        'states': states
    }, context_instance=RequestContext(request))


def bloodcenters_by_state(request, state):
    bloodcenters = BloodCenter.objects.filter(
        address__state=state).order_by('name')
    states = Address.objects.values('state').distinct().order_by('state')
    return render_to_response('bloodcenters/bloodcenters_list.html', {
        'bloodcenters': bloodcenters,
        'states': states
    }, context_instance=RequestContext(request))


def bloodcenter_detail(request, slug):
    bloodcenter = get_object_or_404(BloodCenter, slug=slug)
    return render_to_response('bloodcenters/bloodcenter_detail.html', {
        'bloodcenter': bloodcenter
    }, context_instance=RequestContext(request))
