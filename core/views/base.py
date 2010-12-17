from django.shortcuts import render_to_response
from django.template.context import RequestContext



def index(request):
    return render_to_response('core/home.html', {}, context_instance=RequestContext(request))

def server_error(request):
    return render_to_response('500.html', {}, RequestContext(request))