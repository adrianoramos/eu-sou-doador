from django.shortcuts import render_to_response
from django.template import RequestContext

# from accounts.models import UserProfile

def index(request):
    # total_donors = UserProfile.objects.count()
    return render_to_response('home/index.html',
        # {'total_donors': total_donors},
        context_instance=RequestContext(request))